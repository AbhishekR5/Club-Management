# -*- coding: utf-8 -*-

{
    "name": "Club Committee Management",
    "version": "19.0.1.0.0",
    "summary": "Membership Committee Management for Samruddhi Avenue Club",
    "description": """
Club Committee Management

This module manages:

* Membership Committees
* Committee Members
* Membership Reviews
* Interview Scheduling
* Committee Meetings
* Review Decisions
* Calendar Integration
* Mail Activities
* Email Notifications
* Approval History

Designed for Odoo 19 Community.
""",
    "author": "Samruddhi Avenue Club",
    "website": "",
    "category": "Membership",
    "license": "LGPL-3",
    "application": True,
    "installable": True,
    "depends": [
        "base",
        "mail",
        "calendar",
        "contacts",
        "club_membership",
    ],
    "data": [
        # Security
        "security/security.xml",
        "security/ir.model.access.csv",

        # Data
        "data/sequence.xml",
        "data/activity.xml",
        "data/mail_template.xml",

        # Views
        "views/committee_views.xml",
        "views/committee_member_views.xml",
        "views/review_views.xml",
        "views/meeting_views.xml",
        "views/menu.xml",

        # Reports
        "report/committee_review_report.xml",
        "report/committee_review_templates.xml",
        "report/pending_review_report.xml",
        "report/pending_review_templates.xml",
        "report/interview_schedule_report.xml",
        "report/interview_schedule_templates.xml",
        "report/decision_history_report.xml",
        "report/decision_history_templates.xml",
        "report/approval_statistics_report.xml",
        "report/approval_statistics_templates.xml",
    ],
    "demo": [],
    "images": [],
}