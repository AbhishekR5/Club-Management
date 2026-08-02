# -*- coding: utf-8 -*-

{
    # ── Module Identity ──────────────────────────────────────────────
    "name": "Samruddhi Eco System — Website",
    "version": "19.0.1.0.0",
    "category": "Website",
    "summary": "Premium cinematic website for Samruddhi Eco System",
    "description": """
Samruddhi Eco System — Premium Cinematic Website
=================================================

A production-ready, custom-built cinematic website module for
Samruddhi Eco System on Odoo 19 Community Edition.

Core Architecture
-----------------
* Custom ``http.Controller`` with public website routes
* QWeb templates inheriting ``website.layout``
* 10-file layered SCSS design system (dark cinematic palette)
* Glassmorphism UI with gold accent design tokens
* Modular ES Module JavaScript with component registry
* Google Fonts integration (Inter + Outfit)
* Fully responsive across all breakpoints
* Foundation for Three.js / GSAP / Lenis integration

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
    # website — website.layout, public routing, menu system, SEO
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
        # Layout — master header, footer, SEO, body classes
        "views/layout.xml",

        # Homepage — cinematic landing page (9 sections)
        "views/homepage.xml",

        # Templates — inner page templates (about, ecosystem, etc.)
        "views/templates.xml",
        "views/snippets.xml",
        "views/menus.xml",
    ],

    # ── Assets — Odoo 19 Frontend Asset Pipeline ─────────────────────
    #
    # All assets registered under ``web.assets_frontend`` — the
    # standard bundle for website-facing pages.
    #
    # Load order is critical:
    #   1. Fonts        — Google Fonts @import (must be first)
    #   2. Variables    — SCSS design tokens & CSS custom properties
    #   3. Base         — Reset, dark theme, scrollbar
    #   4. Typography   — Heading scale, display classes, gradient text
    #   5. Layout       — Container, grid, section spacing
    #   6. Components   — Navbar, hero, sections, footer
    #   7. Utilities    — Helper classes, animation-ready states
    #   8. JavaScript   — Core utilities → components → entry point
    #
    # Static images under static/src/img/ are served directly by
    # Odoo's static file handler — no bundle registration needed.
    #
    "assets": {
        "web.assets_frontend": [

            # ── Fonts ────────────────────────────────────────────
            "samruddhi_website/static/src/scss/001_fonts.scss",

            # ── SCSS Design System (load order matters) ──────────
            # 1. Design tokens & CSS custom properties
            "samruddhi_website/static/src/scss/000_variables.scss",
            # 2. Base reset, dark theme, selection, scrollbar
            "samruddhi_website/static/src/scss/010_base.scss",
            # 3. Typography scale, display classes, gradient text
            "samruddhi_website/static/src/scss/020_typography.scss",
            # 4. Container, grid, section spacing, page headers
            "samruddhi_website/static/src/scss/030_layout.scss",
            # 5. Transparent → glassmorphism navbar on scroll
            "samruddhi_website/static/src/scss/040_navbar.scss",
            # 6. Full-viewport hero, CTA buttons, scroll indicator
            "samruddhi_website/static/src/scss/050_hero.scss",
            # 7. Glass cards, pillar cards, stats, CTA section
            "samruddhi_website/static/src/scss/060_sections.scss",
            # 8. Premium 4-column dark footer
            "samruddhi_website/static/src/scss/070_footer.scss",
            # 9. Utilities, animation-ready states, spacing helpers
            "samruddhi_website/static/src/scss/080_utilities.scss",

            # ── JavaScript (ES Modules) ──────────────────────────
            # Core — component registry for lifecycle management
            "samruddhi_website/static/src/js/core/registry.js",
            # Core — DOM helpers, debounce, throttle, viewport
            "samruddhi_website/static/src/js/core/utils.js",
            # Components — navbar scroll-state & mobile menu
            "samruddhi_website/static/src/js/components/navbar.js",
            # Entry point — registers & initializes all components
            "samruddhi_website/static/src/js/main.js",
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
