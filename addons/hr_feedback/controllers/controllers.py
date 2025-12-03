# -*- coding: utf-8 -*-
# from odoo import http


# class HrFeedback(http.Controller):
#     @http.route('/hr_feedback/hr_feedback', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_feedback/hr_feedback/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_feedback.listing', {
#             'root': '/hr_feedback/hr_feedback',
#             'objects': http.request.env['hr_feedback.hr_feedback'].search([]),
#         })

#     @http.route('/hr_feedback/hr_feedback/objects/<model("hr_feedback.hr_feedback"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_feedback.object', {
#             'object': obj
#         })

