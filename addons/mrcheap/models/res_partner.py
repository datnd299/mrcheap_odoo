from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = "res.partner"

    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        related="company_id.currency_id",
        store=True,
        readonly=True,
    )

    debit_balance = fields.Monetary(
        string="Dư nợ",
        currency_field="currency_id",
        compute="_compute_debit_balance",
        store=False,
        compute_sudo=True,  # phòng trường hợp user không xem được account.move
    )


    def _compute_debit_balance(self):
        Move = self.env["account.move"].sudo()
        for partner in self:
            # chỉ lấy hóa đơn bán (out_invoice), đã post, chưa thanh toán
            invoices = Move.search([
                ("partner_id", "=", partner.id),
                ("move_type", "=", "out_invoice"),
                ("state", "=", "posted"),
                ("payment_state", "!=", "paid"),
            ])
            # amount_residual: số tiền còn lại phải thu (theo tiền của move)
            partner.debit_balance = sum(invoices.mapped("amount_residual"))
