# -*- coding: utf-8 -*-
from odoo import http

# class CompanyParser(http.Controller):
#     @http.route('/company_parser/company_parser/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/company_parser/company_parser/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('company_parser.listing', {
#             'root': '/company_parser/company_parser',
#             'objects': http.request.env['company_parser.company_parser'].search([]),
#         })

#     @http.route('/company_parser/company_parser/objects/<model("company_parser.company_parser"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('company_parser.object', {
#             'object': obj
#         })