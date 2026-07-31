# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ClubCommitteeMember(models.Model):
    _name = "club.committee.member"
    _description = "Committee Member"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "committee_id, role, name"
    _rec_name = "name"

    active = fields.Boolean(
        string="Active",
        default=True,
        tracking=True,
    )

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Contact",
        required=True,
        ondelete="restrict",
        tracking=True,
        index=True,
    )

    user_id = fields.Many2one(
        comodel_name="res.users",
        string="System User",
        tracking=True,
        help="Optional user linked to this committee member.",
    )

    name = fields.Char(
        string="Member Name",
        related="partner_id.name",
        store=True,
        readonly=False,
        tracking=True,
        index=True,
    )

    email = fields.Char(
        string="Email",
        related="partner_id.email",
        store=True,
        readonly=False,
        tracking=True,
    )

    phone = fields.Char(
        string="Phone",
        related="partner_id.phone",
        store=True,
        readonly=False,
        tracking=True,
    )

    mobile = fields.Char(
        string="Mobile",
        related="partner_id.mobile",
        store=True,
        readonly=False,
        tracking=True,
    )

    designation = fields.Char(
        string="Designation",
        related="partner_id.function",
        store=True,
        readonly=False,
        tracking=True,
    )

    role = fields.Selection(
        [
            ("chairperson", "Chairperson"),
            ("secretary", "Secretary"),
            ("member", "Member"),
        ],
        string="Role",
        required=True,
        default="member",
        tracking=True,
    )

    committee_id = fields.Many2one(
        comodel_name="club.committee",
        string="Committee",
        required=True,
        ondelete="cascade",
        tracking=True,
        index=True,
    )

    review_ids = fields.One2many(
        comodel_name="club.review",
        inverse_name="committee_member_id",
        string="Assigned Reviews",
    )

    review_count = fields.Integer(
        string="Reviews",
        compute="_compute_review_count",
    )

    color = fields.Integer(
        string="Color Index",
    )

    _sql_constraints = [
        (
            "committee_partner_unique",
            "unique(committee_id, partner_id)",
            "This contact is already a member of this committee.",
        ),
    ]

    @api.depends("review_ids")
    def _compute_review_count(self):
        for record in self:
            record.review_count = len(record.review_ids)

    @api.constrains("role", "committee_id", "active")
    def _check_unique_roles(self):
        for record in self:
            if (
                not record.active
                or record.role not in ("chairperson", "secretary")
            ):
                continue

            duplicate = self.search(
                [
                    ("id", "!=", record.id),
                    ("committee_id", "=", record.committee_id.id),
                    ("role", "=", record.role),
                    ("active", "=", True),
                ],
                limit=1,
            )

            if duplicate:
                raise ValidationError(
                    "Only one %s is allowed per committee."
                    % dict(self._fields["role"].selection)[record.role]
                )

    def action_view_reviews(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": "Membership Reviews",
            "res_model": "club.review",
            "view_mode": "list,form,kanban",
            "domain": [("committee_member_id", "=", self.id)],
            "context": {
                "default_committee_member_id": self.id,
            },
        }