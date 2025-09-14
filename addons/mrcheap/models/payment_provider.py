from odoo import models, _
from urllib.parse import quote_plus

class PaymentProvider(models.Model):
    _inherit = 'payment.provider'