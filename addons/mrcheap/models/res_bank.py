# -*- coding: utf-8 -*-
from odoo import fields, models

class ResBank(models.Model):
    _inherit = "res.bank"

    # Mã ngân hàng dùng cho img.vietqr.io, ví dụ: VCB, TCB, ACB, BIDV...
    vietqr_code = fields.Char(
        string="VietQR Code",
        help="Mã bank cho VietQR (ví dụ: VCB, TCB, ACB...). Dùng để render ảnh QR.",
    )
