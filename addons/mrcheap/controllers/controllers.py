# -*- coding: utf-8 -*-
from odoo import http, fields
from odoo.http import request, Response
import json
import logging
from werkzeug.exceptions import BadRequest

_logger = logging.getLogger(__name__)
import re

class Mrcheap(http.Controller):
    @http.route(['/mrcheap/payment_status/<int:tx_id>'], type='http', auth='public', methods=['GET'], csrf=False,
                sitemap=False)
    def mrcheap_payment_status(self, tx_id, access_token=None, **kw):
        """Trả về trạng thái của payment.transaction theo tx_id.
           Gợi ý: nếu bạn có access_token (của invoice/SO), hãy tự kiểm tra hợp lệ     ở đây để tăng bảo mật."""
        tx = request.env['payment.transaction'].sudo().browse(tx_id)
        if not tx.exists():
            return Response(json.dumps({'ok': False, 'error': 'not_found'}), content_type='application/json')
        invoice = tx.invoice_ids[:1]
        if not invoice or access_token != invoice._portal_ensure_token():
            return Response(json.dumps({'ok': False, 'error': 'unauthorized'}),
                            content_type='application/json', status=403)
        data = {
            'ok': True,
            'id': tx.id,
            'a': invoice._portal_ensure_token(),
            'state': tx.state,
            'invoice_state': invoice.state,
            'invoice_payment_state': invoice.payment_state,
            'amount': tx.amount,
            'currency': tx.currency_id and tx.currency_id.name,
            'reference': tx.reference,
        }
        return Response(json.dumps(data), content_type='application/json', headers=[('Cache-Control', 'no-store')])

    @http.route('/bank/webhook/<int:journal_id>', type='json', auth='public', methods=['POST'], csrf=False)
    def bank_webhook(self, journal_id=None, **kw):
        try:
            payload = json.loads(request.httprequest.data.decode('utf-8')) if request.httprequest.data else {}
        except (json.JSONDecodeError, UnicodeDecodeError):
            payload = {}
        if not payload:
            payload = kw
        """Nhận webhook từ bank khi chuyển khoản thành công."""
        _logger.info("Bank webhook received: %s", payload)
        journal = request.env['account.journal'].sudo().browse(journal_id)
        if not journal.exists() or journal.type != 'bank':
            return {"ok": False, "error": "invalid_journal"}

        token = request.httprequest.headers.get('Authorization', '')
        token = token.replace('Apikey ', '', 1)
        if journal.webhook_token != token:
            return {"ok": False, "error": "invalid_token"}
        if payload.get('transferType') != 'in':
            return {"ok": False, "error": "invalid type"}

        reference = payload.get('content')  # nội dung chuyển khoản (communication)
        amount = payload.get('transferAmount')
        currency = payload.get('currency', 'VND')

        if not reference or not amount:
            request.httprequest.environ['werkzeug.exception'] = 400
            return {"ok": False, "error": "missing fields"}

        # 3. Tìm transaction (payment.transaction) hoặc invoice
        tx = None
        try:
            match = re.search(r'PTRX(\d+)PTRX', reference)
            if match:
                tx_id_str = match.group(1)
                tx_id = int(tx_id_str)
                tx = request.env['payment.transaction'].sudo().browse(tx_id)
                if not tx.exists():
                    tx = None
            if not tx:
                tx = request.env['payment.transaction'].sudo().search([
                    ('reference', '=', reference),
                    ('state', 'in', ['pending', 'draft']),
                ], limit=1)

        except (ValueError, TypeError):
            _logger.warning("Invalid reference format: %s", reference)
            return {"ok": False, "error": "invalid_reference_format"}

        if not tx:
            return {"ok": False, "error": "transaction_not_found"}

        tx.write({
            'state': 'done',
            'last_state_change': fields.Datetime.now(),
        })
        _logger.info("aaaaaaaaaaa: %s", tx.invoice_ids)
        if tx.invoice_ids:
            for inv in tx.invoice_ids:
                payment = request.env['account.payment'].sudo().create({
                    'amount': amount,
                    'currency_id': inv.currency_id.id,
                    'payment_type': 'inbound',
                    'partner_type': 'customer',
                    'partner_id': inv.partner_id.id,
                    'journal_id': request.env['account.journal'].sudo().search([
                        ('type', '=', 'bank'),
                        ('company_id', '=', inv.company_id.id)
                    ], limit=1).id,
                    'date': fields.Date.today(),
                })
                payment.action_post()
                # reconcile
                payment_lines = payment.move_id.line_ids.filtered(
                    lambda line: line.account_id.account_type == 'asset_receivable')
                invoice_lines = inv.line_ids.filtered(lambda line: line.account_id.account_type == 'asset_receivable')
                (payment_lines + invoice_lines).reconcile()

        return {"ok": True}