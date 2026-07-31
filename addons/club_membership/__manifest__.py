# -*- coding: utf-8 -*-

{
    "name": "Club Membership",
    "version": "19.0.1.0.0",
    "summary": "Club Membership Management for Samruddhi Avenue Club",
    "description": """
Club Membership Management

Features
========
* Membership Tier Management
* Member Registration
* Family Members
* Automatic Member ID Generation
* Membership Expiry Management
* Daily Expiry Cron
* Chatter Integration
* Smart Buttons
    """,
    "author": "Samruddhi Avenue Club",
    "website": "",
    "category": "Services",
    "license": "LGPL-3",
    "depends": [
        "base",
        "mail",
        "contacts",
    ],
    "data": [
        "security/ir.model.access.csv",

        #"data/member_sequence.xml",
        #"data/cron.xml",
        #"data/mail_template.xml",

        "views/membership_tier_views.xml",
        "views/family_views.xml",
        "views/member_views.xml",
        #"views/search_views.xml",
        "views/menu.xml",
    ],
    "demo": [],
    "installable": True,
    "application": True,
    "auto_install": False,
}