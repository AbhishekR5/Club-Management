# -*- coding: utf-8 -*-

from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ClubCommitteeMeeting(models.Model):
    _name = "club.committee.meeting"
    _description = "Committee Meeting"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "meeting_date desc, meeting_number desc"
    _rec_name = "meeting_number"

    # ---------------------------------------------------------
    # Basic Information
    # ---------------------------------------------------------

    active = fields.Boolean(
        string="Active",
        default=True,
        tracking=True,
    )

    meeting_number = fields.Char(
        string="Meeting Number",
        required=True,
        readonly=True,
        copy=False,
        default="New",
        tracking=True,
        index=True,
    )

    committee_id = fields.Many2one(
        comodel_name="club.committee",
        string="Committee",
        required=True,
        ondelete="restrict",
        tracking=True,
        index=True,
    )

    meeting_date = fields.Date(
        string="Meeting Date",
        required=True,
        default=fields.Date.context_today,
        tracking=True,
    )

    start_datetime = fields.Datetime(
        string="Start Time",
        required=True,
        tracking=True,
    )

    end_datetime = fields.Datetime(
        string="End Time",
        tracking=True,
    )

    location = fields.Char(
        string="Location",
        tracking=True,
    )

    agenda = fields.Html(
        string="Agenda",
    )

    minutes = fields.Html(
        string="Minutes",
    )

    status = fields.Selection(
        [
            ("draft", "Draft"),
            ("scheduled", "Scheduled"),
            ("in_progress", "In Progress"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        default="draft",
        required=True,
        tracking=True,
        index=True,
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    member_ids = fields.Many2many(
        comodel_name="club.committee.member",
        relation="club_committee_meeting_member_rel",
        column1="meeting_id",
        column2="member_id",
        string="Committee Members",
        tracking=True,
    )

    review_ids = fields.One2many(
        comodel_name="club.review",
        inverse_name="meeting_id",
        string="Membership Reviews",
    )

    calendar_event_id = fields.Many2one(
        comodel_name="calendar.event",
        string="Calendar Event",
        readonly=True,
        copy=False,
    )

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    member_count = fields.Integer(
        string="Members",
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

    # ---------------------------------------------------------
    # Constraints
    # ---------------------------------------------------------

    _sql_constraints = [
        (
            "meeting_number_unique",
            "unique(meeting_number)",
            "Meeting Number must be unique.",
        ),
    ]

    @api.depends("member_ids", "review_ids")
    def _compute_counts(self):
        for meeting in self:
            meeting.member_count = len(meeting.member_ids)
            meeting.review_count = len(meeting.review_ids)
            meeting.applicant_count = len(
                meeting.review_ids.mapped("applicant_id")
            )

    @api.onchange("committee_id")
    def _onchange_committee(self):
        if self.committee_id:
            self.member_ids = [(6, 0, self.committee_id.member_ids.ids)]

    @api.onchange("start_datetime")
    def _onchange_start_datetime(self):
        if self.start_datetime and not self.end_datetime:
            start = fields.Datetime.to_datetime(self.start_datetime)
            self.end_datetime = start + timedelta(hours=2)

    @api.constrains("meeting_date")
    def _check_meeting_date(self):
        today = fields.Date.context_today(self)

        for record in self:
            if (
                record.status != "draft"
                and record.meeting_date
                and record.meeting_date < today
            ):
                raise ValidationError(
                    _("Meeting Date cannot be in the past.")
                )

    @api.constrains("start_datetime", "end_datetime")
    def _check_meeting_time(self):
        for record in self:
            if (
                record.start_datetime
                and record.end_datetime
                and record.end_datetime <= record.start_datetime
            ):
                raise ValidationError(
                    _("End Time must be after Start Time.")
                )

    # ---------------------------------------------------------
    # ORM
    # ---------------------------------------------------------

    @api.model_create_multi
    def create(self, vals_list):
        sequence = self.env["ir.sequence"]

        for vals in vals_list:
            if vals.get("meeting_number", "New") == "New":
                vals["meeting_number"] = (
                    sequence.next_by_code(
                        "club.committee.meeting"
                    )
                    or "New"
                )

        return super().create(vals_list)

    # ---------------------------------------------------------
    # Workflow
    # ---------------------------------------------------------

    def action_schedule(self):
        self.write({
            "status": "scheduled",
        })

        self.message_post(
            body=_("Meeting scheduled.")
        )

    def action_start(self):
        self.write({
            "status": "in_progress",
        })

        self.message_post(
            body=_("Meeting started.")
        )

    def action_complete(self):
        self.write({
            "status": "completed",
        })

        self.message_post(
            body=_("Meeting completed.")
        )

    def action_cancel(self):
        self.write({
            "status": "cancelled",
        })

        self.message_post(
            body=_("Meeting cancelled.")
        )

    def action_reset_to_draft(self):
        self.write({
            "status": "draft",
        })

    # ---------------------------------------------------------
    # Smart Buttons
    # ---------------------------------------------------------

    def action_view_reviews(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": _("Membership Reviews"),
            "res_model": "club.review",
            "view_mode": "list,form,kanban",
            "domain": [("meeting_id", "=", self.id)],
            "context": {
                "default_meeting_id": self.id,
            },
        }

    def action_view_committee(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": _("Committee"),
            "res_model": "club.committee",
            "res_id": self.committee_id.id,
            "view_mode": "form",
            "target": "current",
        }

    # ---------------------------------------------------------
    # Utilities
    # ---------------------------------------------------------

    def copy(self, default=None):
        default = dict(default or {})

        default.update({
            "meeting_number": "New",
            "status": "draft",
            "calendar_event_id": False,
        })

        return super().copy(default)

    def unlink(self):
        for record in self:
            if record.status not in ("draft", "cancelled"):
                raise ValidationError(
                    _(
                        "Only Draft or Cancelled meetings can be deleted."
                    )
                )

        return super().unlink()