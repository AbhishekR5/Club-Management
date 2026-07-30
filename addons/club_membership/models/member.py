# -*- coding: utf-8 -*-

from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ClubMember(models.Model):
    _name = "club.member"
    _description = "Club Member"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "member_id desc"
    _rec_name = "name"

    member_id = fields.Char(
        string="Member ID",
        required=True,
        readonly=True,
        copy=False,
        default="New",
        index=True,
        tracking=True,
    )

    name = fields.Char(
        string="Member Name",
        required=True,
        tracking=True,
        index=True,
    )

    image_1920 = fields.Image(
        string="Photo",
        max_width=1920,
        max_height=1920,
    )

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Contact",
        required=True,
        ondelete="restrict",
        tracking=True,
        index=True,
    )

    membership_tier_id = fields.Many2one(
        comodel_name="club.membership.tier",
        string="Membership Tier",
        required=True,
        ondelete="restrict",
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

    mobile = fields.Char(
        string="Mobile",
        store=True,
        readonly=False,
        tracking=True,
        required=True,
    )

    phone = fields.Char(
        string="Phone",
        related="partner_id.phone",
        store=True,
        readonly=False,
    )

    date_of_birth = fields.Date(
        string="Date of Birth",
    )

    gender = fields.Selection(
        [
            ("male", "Male"),
            ("female", "Female"),
            ("other", "Other"),
        ],
        string="Gender",
    )

    blood_group = fields.Selection(
        [
            ("A+", "A+"),
            ("A-", "A-"),
            ("B+", "B+"),
            ("B-", "B-"),
            ("AB+", "AB+"),
            ("AB-", "AB-"),
            ("O+", "O+"),
            ("O-", "O-"),
        ],
        string="Blood Group",
    )

    occupation = fields.Char(
        string="Occupation",
    )

    company = fields.Char(
        string="Company",
    )

    street = fields.Char(
        string="Address",
        related="partner_id.street",
        store=True,
        readonly=False,
    )

    street2 = fields.Char(
        string="Address Line 2",
        related="partner_id.street2",
        store=True,
        readonly=False,
    )

    city = fields.Char(
        string="City",
        related="partner_id.city",
        store=True,
        readonly=False,
    )

    state_id = fields.Many2one(
        comodel_name="res.country.state",
        string="State",
        related="partner_id.state_id",
        store=True,
        readonly=False,
    )

    country_id = fields.Many2one(
        comodel_name="res.country",
        string="Country",
        related="partner_id.country_id",
        store=True,
        readonly=False,
    )

    zip = fields.Char(
        string="Pincode",
        related="partner_id.zip",
        store=True,
        readonly=False,
    )

    joining_date = fields.Date(
        string="Joining Date",
        required=True,
        default=fields.Date.context_today,
        tracking=True,
    )

    expiry_date = fields.Date(
        string="Expiry Date",
        required=True,
        tracking=True,
    )

    status = fields.Selection(
        [
            ("draft", "Draft"),
            ("pending", "Pending"),
            ("active", "Active"),
            ("suspended", "Suspended"),
            ("expired", "Expired"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        default="draft",
        required=True,
        tracking=True,
        index=True,
    )

    notes = fields.Html(
        string="Internal Notes",
    )

    family_member_ids = fields.One2many(
        comodel_name="club.family.member",
        inverse_name="member_id",
        string="Family Members",
    )

    family_member_count = fields.Integer(
        string="Family Members",
        compute="_compute_family_member_count",
    )

    active = fields.Boolean(
        string="Active",
        default=True,
    )

    _sql_constraints = [
        (
            "club_member_member_id_unique",
            "unique(member_id)",
            "Member ID must be unique.",
        ),
        (
            "club_member_email_unique",
            "unique(email)",
            "Email address already exists.",
        ),
    ]

    @api.depends("family_member_ids")
    def _compute_family_member_count(self):
        for record in self:
            record.family_member_count = len(record.family_member_ids)

    @api.onchange("joining_date")
    def _onchange_joining_date(self):
        """Automatically set expiry date to one year from joining date."""
        if self.joining_date:
            self.expiry_date = self.joining_date + timedelta(days=365)

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        """Populate member name from selected partner if empty."""
        if self.partner_id and not self.name:
            self.name = self.partner_id.name

    @api.constrains("email")
    def _check_unique_email(self):
        for record in self:
            if not record.email:
                continue

            duplicate = self.search(
                [
                    ("id", "!=", record.id),
                    ("email", "=", record.email),
                ],
                limit=1,
            )
            if duplicate:
                raise ValidationError(
                    "Email address already exists."
                )

    @api.constrains("mobile")
    def _check_mobile(self):
        for record in self:
            if not record.mobile:
                raise ValidationError(
                    "Mobile number is required."
                )

    @api.constrains("joining_date")
    def _check_joining_date(self):
        today = fields.Date.context_today(self)

        for record in self:
            if (
                record.joining_date
                and record.joining_date > today
            ):
                raise ValidationError(
                    "Joining Date cannot be later than today's date."
                )

    @api.constrains("joining_date", "expiry_date")
    def _check_expiry_date(self):
        for record in self:
            if (
                record.joining_date
                and record.expiry_date
                and record.expiry_date <= record.joining_date
            ):
                raise ValidationError(
                    "Expiry Date must be after Joining Date."
                )

    @api.constrains("date_of_birth")
    def _check_date_of_birth(self):
        today = fields.Date.context_today(self)

        for record in self:
            if (
                record.date_of_birth
                and record.date_of_birth > today
            ):
                raise ValidationError(
                    "Date of Birth cannot be in the future."
                )

    @api.constrains("partner_id")
    def _check_partner(self):
        for record in self:
            if not record.partner_id:
                raise ValidationError(
                    "Contact is required."
                )

    @api.constrains("membership_tier_id")
    def _check_membership_tier(self):
        for record in self:
            if not record.membership_tier_id:
                raise ValidationError(
                    "Membership Tier is required."
                )

    @api.model_create_multi
    def create(self, vals_list):
        sequence = self.env["ir.sequence"]

        for vals in vals_list:
            if vals.get("member_id", "New") == "New":
                vals["member_id"] = sequence.next_by_code("club.member") or "New"

            joining_date = vals.get("joining_date")
            expiry_date = vals.get("expiry_date")

            if joining_date and not expiry_date:
                joining = fields.Date.to_date(joining_date)
                vals["expiry_date"] = joining + timedelta(days=365)

        records = super().create(vals_list)
        return records

    def write(self, vals):
        if "joining_date" in vals and "expiry_date" not in vals:
            joining = fields.Date.to_date(vals["joining_date"])
            vals["expiry_date"] = joining + timedelta(days=365)

        return super().write(vals)

    @api.model
    def cron_update_expired_members(self):
        today = fields.Date.context_today(self)

        expired_members = self.search([
            ("status", "!=", "expired"),
            ("status", "!=", "cancelled"),
            ("expiry_date", "<", today),
        ])

        if expired_members:
            expired_members.write({
                "status": "expired",
            })

    def action_view_family_members(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": "Family Members",
            "res_model": "club.family.member",
            "view_mode": "list,form",
            "domain": [("member_id", "=", self.id)],
            "context": {
                "default_member_id": self.id,
            },
        }

    def action_activate(self):
        self.write({
            "status": "active",
        })

    def action_suspend(self):
        self.write({
            "status": "suspended",
        })

    def action_cancel(self):
        self.write({
            "status": "cancelled",
        })

    def action_reset_to_draft(self):
        self.write({
            "status": "draft",
        })