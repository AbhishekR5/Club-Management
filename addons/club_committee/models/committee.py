# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ClubCommittee(models.Model):
    _name = "club.committee"
    _description = "Club Committee"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name"

    active = fields.Boolean(
        string="Active",
        default=True,
        tracking=True,
    )

    name = fields.Char(
        string="Committee Name",
        required=True,
        tracking=True,
        index=True,
    )

    description = fields.Text(
        string="Description",
    )

    chairperson_id = fields.Many2one(
        comodel_name="club.committee.member",
        string="Chairperson",
        domain="[('role','=','chairperson'), ('committee_id','=',id)]",
        tracking=True,
    )

    secretary_id = fields.Many2one(
        comodel_name="club.committee.member",
        string="Secretary",
        domain="[('role','=','secretary'), ('committee_id','=',id)]",
        tracking=True,
    )

    member_ids = fields.Many2many(
        comodel_name="club.committee.member",
        relation="club_committee_member_rel",
        column1="committee_id",
        column2="member_id",
        string="Committee Members",
        tracking=True,
    )

    meeting_frequency = fields.Selection(
        [
            ("weekly", "Weekly"),
            ("fortnightly", "Fortnightly"),
            ("monthly", "Monthly"),
            ("quarterly", "Quarterly"),
            ("half_yearly", "Half Yearly"),
            ("yearly", "Yearly"),
        ],
        string="Meeting Frequency",
        default="monthly",
        required=True,
        tracking=True,
    )

    meeting_count = fields.Integer(
        string="Meetings",
        compute="_compute_counts",
    )

    review_count = fields.Integer(
        string="Reviews",
        compute="_compute_counts",
    )

    applicant_count = fields.Integer(
        string="Applicants",
        compute="_compute_counts",
    )

    meeting_ids = fields.One2many(
        comodel_name="club.committee.meeting",
        inverse_name="committee_id",
        string="Meetings",
    )

    review_ids = fields.One2many(
        comodel_name="club.review",
        inverse_name="committee_id",
        string="Membership Reviews",
    )

    @api.depends("member_ids")
    def _compute_counts(self):
        Meeting = self.env["club.committee.meeting"]
        Review = self.env["club.review"]

        for committee in self:
            committee.meeting_count = Meeting.search_count([
                ("committee_id", "=", committee.id)
            ])

            committee.review_count = Review.search_count([
                ("committee_id", "=", committee.id)
            ])

            committee.applicant_count = Review.search_count([
                ("committee_id", "=", committee.id)
            ])

    def action_view_meetings(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": "Meetings",
            "res_model": "club.committee.meeting",
            "view_mode": "list,form,calendar",
            "domain": [("committee_id", "=", self.id)],
            "context": {
                "default_committee_id": self.id,
            },
        }

    def action_view_reviews(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": "Membership Reviews",
            "res_model": "club.review",
            "view_mode": "list,kanban,form,calendar",
            "domain": [("committee_id", "=", self.id)],
            "context": {
                "default_committee_id": self.id,
            },
        }

    def action_view_applicants(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": "Applicants",
            "res_model": "club.member",
            "view_mode": "list,form",
            "domain": [
                ("id", "in",
                 self.env["club.review"].search([
                     ("committee_id", "=", self.id)
                 ]).mapped("applicant_id").ids)
            ],
        }