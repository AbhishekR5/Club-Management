# -*- coding: utf-8 -*-

{
    # ── Module Identity ──────────────────────────────────────────────
    "name": "Samruddhi Website 3D",
    "version": "19.0.1.0.0",
    "category": "Website",
    "summary": "Premium 3D cinematic website for Samruddhi Eco System",
    "description": """
Samruddhi Website 3D
=====================

A production-ready, premium cinematic website module for the
Samruddhi Eco System, built on Odoo 19 Community Edition.

Core Architecture
-----------------
* Custom ``http.Controller`` with public website routes
* QWeb templates inheriting ``website.layout``
* Layered SCSS design system via ``web.assets_frontend``
* Modular ES Module JavaScript foundation
* Google Fonts integration (Inter + Outfit)
* Prepared for Three.js / GSAP / Lenis integration

Technical Stack
---------------
* Backend: Odoo 19 Community, Python 3.12, PostgreSQL
* Frontend: HTML5, SCSS, Vanilla JavaScript (ES Modules)
* Asset Pipeline: Odoo 19 ``web.assets_frontend`` bundle
    """,

    # ── Author & License ─────────────────────────────────────────────
    "author": "Samruddhi Avenue Club",
    "website": "",
    "license": "LGPL-3",

    # ── Dependencies ─────────────────────────────────────────────────
    #
    # website — provides website.layout, public routing, menu system
    # web     — core asset pipeline, frontend framework, SCSS compiler
    # mail    — chatter, activity tracking, email notifications
    #
    "depends": [
        "website",
        "web",
        "mail",
    ],

    # ── Data Files (loaded on install & upgrade) ─────────────────────
    "data": [
        # Security — Access Control Lists
        "security/ir.model.access.csv",

        # Views — Backend views & website menus
        "views/website_menus.xml",

        # Templates — QWeb frontend pages
        "templates/homepage_template.xml",
        "templates/page_templates.xml",
    ],

    # ── Assets — Odoo 19 Frontend Asset Pipeline ─────────────────────
    #
    # All assets are registered under ``web.assets_frontend`` which
    # is the standard bundle for website-facing pages.
    #
    # Load order:
    #   1. Fonts (external Google Fonts import)
    #   2. SCSS variables & design tokens
    #   3. SCSS base reset & defaults
    #   4. SCSS layout system
    #   5. JavaScript entry point
    #
    # Images under static/src/img/ are served directly by Odoo's
    # static file handler and do not need bundle registration.
    #
    "assets": {
        "web.assets_frontend": [

            # ── Fonts ────────────────────────────────────────────
            # Google Fonts (Inter + Outfit) loaded via @import
            "samruddhi_website_3d/static/src/scss/fonts.scss",

            # ── SCSS Design System ───────────────────────────────
            # Variables & tokens MUST load first (other files depend on them)
            "samruddhi_website_3d/static/src/scss/variables.scss",
            # Base reset, typography defaults, scrollbar, selection
            "samruddhi_website_3d/static/src/scss/base.scss",
            # Container, grid, section spacing, hero, page headers
            "samruddhi_website_3d/static/src/scss/layout.scss",

            # ── JavaScript (ES Modules) ──────────────────────────
            # Main entry point — registers & initializes all components
            "samruddhi_website_3d/static/src/js/main.js",
        ],
    },

    # ── Images ───────────────────────────────────────────────────────
    # Module icon displayed in the Odoo Apps list
    "images": [
        "static/description/icon.png",
    ],

    # ── Module Flags ─────────────────────────────────────────────────
    "installable": True,
    "application": True,
    "auto_install": False,

    # ── No demo data ─────────────────────────────────────────────────
    "demo": [],
}
