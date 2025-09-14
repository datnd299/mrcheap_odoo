# -*- coding: utf-8 -*-
from odoo import models, fields

class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_portal_payment_url(self):
        ICP = self.env["ir.config_parameter"].sudo()
        base = ICP.get_param("web.base.url", "")
        self.ensure_one()
        if self.move_type in ("out_invoice", "out_refund"):
            token = self._portal_ensure_token()
            return f"{base}/my/invoices/{self.id}?access_token={token}"
        return ""

    def action_get_payment_link(self):
        self.ensure_one()
        url = self._get_portal_payment_url()
        return {
            "type": "ir.actions.client",
            "tag": "mrcheap_copy_link",        # JS sẽ handle tag này
            "params": {"url": url},
        }
