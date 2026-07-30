# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ClubMembershipTier(models.Model):
    _name = "club.membership.tier"
    _description = "Membership Tier"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "sequence, name"
    _rec_name = "name"

    name = fields.Char(
        string="Membership Tier",
        required=True,
        tracking=True,
        index=True,
    )

    joining_fee = fields.Monetary(
        string="Joining Fee",
        required=True,
        default=0.0,
        tracking=True,
        currency_field="currency_id",
    )

    annual_renewal_fee = fields.Monetary(
        string="Annual Renewal Fee",
        required=True,
        default=0.0,
        tracking=True,
        currency_field="currency_id",
    )

    description = fields.Text(
        string="Description",
    )

    active = fields.Boolean(
        string="Active",
        default=True,
        tracking=True,
    )

    sequence = fields.Integer(
        string="Sequence",
        default=10,
        index=True,
    )

    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        required=True,
        default=lambda self: self.env.company.currency_id.id,
    )

    member_ids = fields.One2many(
        comodel_name="club.member",
        inverse_name="membership_tier_id",
        string="Members",
    )

    member_count = fields.Integer(
        string="Members",
        compute="_compute_member_count",
        store=False,
    )

    _sql_constraints = [
        (
            "club_membership_tier_name_unique",
            "unique(name)",
            "Membership Tier name must be unique.",
        ),
        (
            "club_membership_tier_joining_fee_check",
            "CHECK(joining_fee >= 0)",
            "Joining Fee cannot be negative.",
        ),
        (
            "club_membership_tier_renewal_fee_check",
            "CHECK(annual_renewal_fee >= 0)",
            "Annual Renewal Fee cannot be negative.",
        ),
    ]

    @api.depends("member_ids")
    def _compute_member_count(self):
        for record in self:
            record.member_count = len(record.member_ids)

    @api.constrains("name")
    def _check_name(self):
        for record in self:
            if not record.name or not record.name.strip():
                raise ValidationError("Membership Tier name cannot be empty.")

    def action_view_members(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Members",
            "res_model": "club.member",
            "view_mode": "list,form,kanban",
            "domain": [("membership_tier_id", "=", self.id)],
            "context": {
                "default_membership_tier_id": self.id,
            },
        }