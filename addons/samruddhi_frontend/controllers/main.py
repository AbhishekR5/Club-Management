# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class FrontendController(http.Controller):
    @http.route('/', auth='public', website=True)
    def homepage(self, **kw):
        return request.render('samruddhi_frontend.homepage', {})
