# -*- coding: utf-8 -*-
# from odoo import http


# class Mrcheap(http.Controller):
#     @http.route('/mrcheap/mrcheap', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mrcheap/mrcheap/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mrcheap.listing', {
#             'root': '/mrcheap/mrcheap',
#             'objects': http.request.env['mrcheap.mrcheap'].search([]),
#         })

#     @http.route('/mrcheap/mrcheap/objects/<model("mrcheap.mrcheap"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mrcheap.object', {
#             'object': obj
#         })

