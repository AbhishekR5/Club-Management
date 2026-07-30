# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ClubFamilyMember(models.Model):
    _name = "club.family.member"
    _description = "Club Family Member"
    _order = "name"

    name = fields.Char(
        string="Name",
        required=True,
        index=True,
    )

    member_id = fields.Many2one(
        comodel_name="club.member",
        string="Linked Member",
        required=True,
        ondelete="cascade",
        index=True,
    )

    relation = fields.Selection(
        selection=[
            ("spouse", "Spouse"),
            ("father", "Father"),
            ("mother", "Mother"),
            ("son", "Son"),
            ("daughter", "Daughter"),
            ("brother", "Brother"),
            ("sister", "Sister"),
            ("guardian", "Guardian"),
            ("other", "Other"),
        ],
        string="Relation",
        required=True,
    )

    date_of_birth = fields.Date(
        string="Date of Birth",
    )

    phone = fields.Char(
        string="Phone",
        required=True,
    )

    email = fields.Char(
        string="Email",
    )

    active = fields.Boolean(
        string="Active",
        default=True,
    )

    _sql_constraints = [
        (
            "club_family_member_phone_member_unique",
            "unique(member_id, phone)",
            "This phone number already exists for this member.",
        ),
    ]

    @api.constrains("email")
    def _check_email(self):
        for record in self:
            if record.email:
                email = record.email.strip().lower()
                duplicate = self.search(
                    [
                        ("id", "!=", record.id),
                        ("email", "=", email),
                    ],
                    limit=1,
                )
                if duplicate:
                    raise ValidationError(
                        "Family member email address must be unique."
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

    @api.constrains("phone")
    def _check_phone(self):
        for record in self:
            if not record.phone or not record.phone.strip():
                raise ValidationError(
                    "Phone number is required."
                )

    @api.onchange("email")
    def _onchange_email(self):
        if self.email:
            self.email = self.email.strip().lower()