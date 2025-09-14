from odoo import api, fields, models

class AccountJournal(models.Model):
    _inherit = "account.journal"

    webhook_token = fields.Char(
        string="Webhook Token",
        help="Token dùng để xác thực webhook ngân hàng",
    )

    webhook_url = fields.Char(string='Webhook URL', compute='_compute_webhook_url', readonly=True)

    def _compute_webhook_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for record in self:
            if record.id:
                record.webhook_url = f"{base_url}/bank/webhook/{record.id}"
            else:
                record.webhook_url = ""
