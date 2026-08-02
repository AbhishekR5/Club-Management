# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class SamruddhiWebsiteController(http.Controller):
    """
    Public-facing controllers for the Samruddhi Eco System website.

    Every route uses:
        - ``type='http'``   — standard HTTP request/response
        - ``auth='public'`` — accessible without login
        - ``website=True``  — inherits website layout, theme, header & footer
        - ``sitemap=True``  — included in /sitemap.xml generation

    Template naming convention:
        ``samruddhi_website.<page_name>``
    """

    # ── Homepage ─────────────────────────────────────────────────────

    @http.route(
        "/",
        type="http",
        auth="public",
        website=True,
        sitemap=True,
    )
    def homepage(self, **kwargs):
        """Cinematic landing page — hero, vision, pillars, stats, CTA."""
        return request.render("samruddhi_website.homepage", {
            "page_class": "se-homepage",
        })

    # ── About ────────────────────────────────────────────────────────

    @http.route(
        "/about",
        type="http",
        auth="public",
        website=True,
        sitemap=True,
    )
    def page_about(self, **kwargs):
        """Our story, vision, mission, and leadership team."""
        return request.render("samruddhi_website.page_about", {
            "page_class": "se-about",
        })

    # ── Ecosystem ────────────────────────────────────────────────────

    @http.route(
        "/ecosystem",
        type="http",
        auth="public",
        website=True,
        sitemap=True,
    )
    def page_ecosystem(self, **kwargs):
        """The four pillars of the Samruddhi Eco System."""
        return request.render("samruddhi_website.page_ecosystem", {
            "page_class": "se-ecosystem",
        })

    # ── Membership ───────────────────────────────────────────────────

    @http.route(
        "/membership",
        type="http",
        auth="public",
        website=True,
        sitemap=True,
    )
    def page_membership(self, **kwargs):
        """Membership tiers, benefits, and application info."""
        return request.render("samruddhi_website.page_membership", {
            "page_class": "se-membership",
        })

    # ── Projects ─────────────────────────────────────────────────────

    @http.route(
        "/projects",
        type="http",
        auth="public",
        website=True,
        sitemap=True,
    )
    def page_projects(self, **kwargs):
        """Showcase of community projects and initiatives."""
        return request.render("samruddhi_website.page_projects", {
            "page_class": "se-projects",
        })

    # ── Contact ──────────────────────────────────────────────────────

    @http.route(
        "/contact",
        type="http",
        auth="public",
        website=True,
        sitemap=True,
    )
    def page_contact(self, **kwargs):
        """Contact form, location, and communication channels."""
        return request.render("samruddhi_website.page_contact", {
            "page_class": "se-contact",
        })
