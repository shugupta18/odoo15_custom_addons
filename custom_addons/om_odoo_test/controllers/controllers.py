# -*- coding: utf-8 -*-
# from odoo import http


# class OmOdooTest(http.Controller):
#     @http.route('/om_odoo_test/om_odoo_test', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/om_odoo_test/om_odoo_test/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('om_odoo_test.listing', {
#             'root': '/om_odoo_test/om_odoo_test',
#             'objects': http.request.env['om_odoo_test.om_odoo_test'].search([]),
#         })

#     @http.route('/om_odoo_test/om_odoo_test/objects/<model("om_odoo_test.om_odoo_test"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('om_odoo_test.object', {
#             'object': obj
#         })
