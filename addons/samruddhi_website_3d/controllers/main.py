# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class SamruddhiWebsite3DController(http.Controller):
    """
    Public website controllers for Samruddhi Website 3D.

    All routes use ``auth='public'`` and ``website=True`` to
    integrate with the Odoo website framework (layout, header,
    footer, and theme).
    """

    @http.route(
        "/samruddhi",
        type="http",
        auth="public",
        website=True,
        sitemap=True,
    )
    def homepage(self, **kwargs):
        """Render the Samruddhi 3D homepage."""
        return request.render("samruddhi_website_3d.homepage", {})

    @http.route(
        "/samruddhi/about",
        type="http",
        auth="public",
        website=True,
        sitemap=True,
    )
    def page_about(self, **kwargs):
        """Render the About page."""
        return request.render("samruddhi_website_3d.page_about", {})

    @http.route(
        "/samruddhi/contact",
        type="http",
        auth="public",
        website=True,
        sitemap=True,
    )
    def page_contact(self, **kwargs):
        """Render the Contact page."""
        return request.render("samruddhi_website_3d.page_contact", {})
