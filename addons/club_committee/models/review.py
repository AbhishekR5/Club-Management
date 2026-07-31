# -*- coding: utf-8 -*-

from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ClubReview(models.Model):
    _name = "club.review"
    _description = "Membership Committee Review"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "review_number desc"
    _rec_name = "review_number"

    # ---------------------------------------------------------
    # Basic Information
    # ---------------------------------------------------------

    active = fields.Boolean(
        string="Active",
        default=True,
        tracking=True,
    )

    review_number = fields.Char(
        string="Review Number",
        required=True,
        readonly=True,
        copy=False,
        default="New",
        index=True,
        tracking=True,
    )

    applicant_id = fields.Many2one(
        comodel_name="club.member",
        string="Applicant",
        required=True,
        ondelete="restrict",
        index=True,
        tracking=True,
    )

    applicant_partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Applicant Contact",
        related="applicant_id.partner_id",
        store=True,
        readonly=True,
    )

    committee_id = fields.Many2one(
        comodel_name="club.committee",
        string="Committee",
        required=True,
        ondelete="restrict",
        tracking=True,
        index=True,
    )

    committee_member_id = fields.Many2one(
        comodel_name="club.committee.member",
        string="Assigned Committee Member",
        domain="[('committee_id','=',committee_id)]",
        tracking=True,
    )

    meeting_id = fields.Many2one(
        comodel_name="club.committee.meeting",
        string="Meeting",
        tracking=True,
        ondelete="set null",
    )

    calendar_event_id = fields.Many2one(
        comodel_name="calendar.event",
        string="Calendar Event",
        readonly=True,
        copy=False,
    )

    approved_by_id = fields.Many2one(
        comodel_name="res.users",
        string="Approved By",
        readonly=True,
        tracking=True,
        copy=False,
    )

    # ---------------------------------------------------------
    # Interview
    # ---------------------------------------------------------

    interview_start = fields.Datetime(
        string="Interview Start",
        tracking=True,
    )

    interview_end = fields.Datetime(
        string="Interview End",
        tracking=True,
    )

    interview_location = fields.Char(
        string="Interview Location",
        tracking=True,
    )

    # ---------------------------------------------------------
    # Decision
    # ---------------------------------------------------------

    recommendation = fields.Selection(
        [
            ("pending", "Pending"),
            ("approve", "Approve"),
            ("reject", "Reject"),
            ("documents", "Need More Documents"),
            ("interview_again", "Interview Again"),
        ],
        string="Recommendation",
        default="pending",
        tracking=True,
        required=True,
        index=True,
    )

    status = fields.Selection(
        [
            ("draft", "Draft"),
            ("scheduled", "Scheduled"),
            ("interview_completed", "Interview Completed"),
            ("under_review", "Under Review"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
            ("returned", "Returned"),
        ],
        string="Status",
        default="draft",
        required=True,
        tracking=True,
        index=True,
    )

    score = fields.Float(
        string="Interview Score",
        digits=(6, 2),
        tracking=True,
    )

    decision_date = fields.Date(
        string="Decision Date",
        tracking=True,
    )

    remarks = fields.Html(
        string="Committee Remarks",
    )

    # ---------------------------------------------------------
    # Related Information
    # ---------------------------------------------------------

    applicant_email = fields.Char(
        string="Applicant Email",
        related="applicant_id.email",
        store=True,
        readonly=True,
    )

    applicant_mobile = fields.Char(
        string="Applicant Mobile",
        related="applicant_id.mobile",
        store=True,
        readonly=True,
    )

    committee_chairperson_id = fields.Many2one(
        related="committee_id.chairperson_id",
        string="Chairperson",
        store=True,
        readonly=True,
    )

    committee_secretary_id = fields.Many2one(
        related="committee_id.secretary_id",
        string="Secretary",
        store=True,
        readonly=True,
    )

    color = fields.Integer(
        string="Color",
    )

    # ---------------------------------------------------------
    # Smart Button Counters
    # ---------------------------------------------------------

    activity_count = fields.Integer(
        string="Activities",
        compute="_compute_counts",
    )

    message_count = fields.Integer(
        string="Messages",
        compute="_compute_counts",
    )

    # ---------------------------------------------------------
    # SQL Constraints
    # ---------------------------------------------------------

    _sql_constraints = [
        (
            "review_number_unique",
            "unique(review_number)",
            "Review Number must be unique.",
        ),
    ]

    # ---------------------------------------------------------
    # Compute Methods
    # ---------------------------------------------------------

    @api.depends("activity_ids", "message_ids")
    def _compute_counts(self):
        for review in self:
            review.activity_count = len(review.activity_ids)
            review.message_count = len(review.message_ids)

    # ---------------------------------------------------------
    # Onchange Methods
    # ---------------------------------------------------------

    @api.onchange("meeting_id")
    def _onchange_meeting(self):
        if self.meeting_id:
            self.committee_id = self.meeting_id.committee_id

    @api.onchange("interview_start")
    def _onchange_interview_start(self):
        """
        Default interview duration to one hour.
        """
        if self.interview_start and not self.interview_end:
            self.interview_end = (
                self.interview_start + timedelta(hours=1)
            )

    # ---------------------------------------------------------
    # ORM Overrides
    # ---------------------------------------------------------

    @api.model_create_multi
    def create(self, vals_list):
        sequence = self.env["ir.sequence"]

        for vals in vals_list:
            if vals.get("review_number", "New") == "New":
                vals["review_number"] = (
                    sequence.next_by_code("club.review")
                    or "New"
                )

        records = super().create(vals_list)

        return records

        # ---------------------------------------------------------
    # Constraints
    # ---------------------------------------------------------

    @api.constrains("interview_start")
    def _check_interview_date(self):
        """Interview cannot be scheduled in the past."""
        now = fields.Datetime.now()

        for record in self:
            if (
                record.interview_start
                and record.status != "draft"
                and record.interview_start < now
            ):
                raise ValidationError(
                    _("Interview date cannot be in the past.")
                )

    @api.constrains("interview_start", "interview_end")
    def _check_interview_duration(self):
        for record in self:
            if (
                record.interview_start
                and record.interview_end
                and record.interview_end <= record.interview_start
            ):
                raise ValidationError(
                    _("Interview End must be after Interview Start.")
                )

    @api.constrains("decision_date", "interview_start")
    def _check_decision_date(self):
        for record in self:
            if (
                record.decision_date
                and record.interview_start
                and record.decision_date
                < record.interview_start.date()
            ):
                raise ValidationError(
                    _("Decision Date cannot be before Interview Date.")
                )

    @api.constrains("applicant_id", "active")
    def _check_active_review(self):
        """
        Only one active review per applicant.
        """

        terminal_states = ("approved", "rejected")

        for record in self:
            duplicate = self.search(
                [
                    ("id", "!=", record.id),
                    ("applicant_id", "=", record.applicant_id.id),
                    ("active", "=", True),
                    ("status", "not in", terminal_states),
                ],
                limit=1,
            )

            if duplicate:
                raise ValidationError(
                    _("Applicant already has an active review.")
                )

    # ---------------------------------------------------------
    # Workflow Buttons
    # ---------------------------------------------------------

    def action_schedule_interview(self):
        for review in self:

            if not review.interview_start:
                raise ValidationError(
                    _("Interview Start is required.")
                )

            review.status = "scheduled"

            review._create_calendar_event()
            review._schedule_activity(
                "Interview Scheduled"
            )

            review.message_post(
                body=_(
                    "Interview has been scheduled."
                )
            )

    def action_complete_interview(self):
        self.write({
            "status": "interview_completed",
        })

        self._schedule_activity(
            "Committee Review"
        )

        self.message_post(
            body=_(
                "Interview completed."
            )
        )

    def action_under_review(self):
        self.write({
            "status": "under_review",
        })

        self._schedule_activity(
            "Decision Pending"
        )

        self.message_post(
            body=_(
                "Application moved for committee review."
            )
        )

    def action_approve(self):

        today = fields.Date.context_today(self)

        self.write({
            "status": "approved",
            "recommendation": "approve",
            "decision_date": today,
            "approved_by_id": self.env.user.id,
        })

        self.applicant_id.write({
            "status": "pending",
        })

        self.activity_unlink()

        self.message_post(
            body=_(
                "Application approved by committee."
            )
        )

    def action_reject(self):

        today = fields.Date.context_today(self)

        self.write({
            "status": "rejected",
            "recommendation": "reject",
            "decision_date": today,
            "approved_by_id": self.env.user.id,
        })

        self.activity_unlink()

        self.message_post(
            body=_(
                "Application rejected."
            )
        )

    def action_return(self):

        self.write({
            "status": "returned",
            "recommendation": "documents",
        })

        self._schedule_activity(
            "Document Verification"
        )

        self.message_post(
            body=_(
                "Application returned for additional documents."
            )
        )

    def action_reset_to_draft(self):

        self.write({
            "status": "draft",
            "recommendation": "pending",
            "approved_by_id": False,
            "decision_date": False,
        })

    # ---------------------------------------------------------
    # Calendar Integration
    # ---------------------------------------------------------

    def _create_calendar_event(self):

        Calendar = self.env["calendar.event"]

        for review in self:

            if review.calendar_event_id:
                continue

            attendee_ids = []

            if review.applicant_partner_id:
                attendee_ids.append(
                    review.applicant_partner_id.id
                )

            for member in review.committee_id.member_ids:
                if member.partner_id:
                    attendee_ids.append(
                        member.partner_id.id
                    )

            stop = review.interview_end

            if not stop:
                start = fields.Datetime.to_datetime(
                    review.interview_start
                )
                stop = start + timedelta(hours=1)

            event = Calendar.create({
                "name": (
                    "Membership Interview - %s"
                    % review.applicant_id.name
                ),
                "start": review.interview_start,
                "stop": stop,
                "location": review.interview_location,
                "partner_ids": [(6, 0, attendee_ids)],
                "description": (
                    "Committee Review Interview"
                ),
            })

            review.calendar_event_id = event.id

    # ---------------------------------------------------------
    # Activities
    # ---------------------------------------------------------

    def _schedule_activity(self, summary):

        activity_type = self.env.ref(
            "mail.mail_activity_data_todo"
        )

        for review in self:

            review.activity_schedule(
                activity_type.id,
                summary=summary,
                user_id=self.env.user.id,
            )

        # ---------------------------------------------------------
    # Calendar Utilities
    # ---------------------------------------------------------

    def action_view_calendar_event(self):
        self.ensure_one()

        if not self.calendar_event_id:
            return False

        return {
            "type": "ir.actions.act_window",
            "name": _("Interview"),
            "res_model": "calendar.event",
            "res_id": self.calendar_event_id.id,
            "view_mode": "form",
            "target": "current",
        }

    def action_view_meeting(self):
        self.ensure_one()

        if not self.meeting_id:
            return False

        return {
            "type": "ir.actions.act_window",
            "name": _("Committee Meeting"),
            "res_model": "club.committee.meeting",
            "res_id": self.meeting_id.id,
            "view_mode": "form",
            "target": "current",
        }

    def action_view_applicant(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": _("Applicant"),
            "res_model": "club.member",
            "res_id": self.applicant_id.id,
            "view_mode": "form",
            "target": "current",
        }

    # ---------------------------------------------------------
    # Helper Methods
    # ---------------------------------------------------------

    def _change_state(
        self,
        status,
        recommendation=None,
        decision=False,
        approved=False,
        message=None,
    ):
        """
        Common workflow helper.
        """

        for review in self:

            values = {
                "status": status,
            }

            if recommendation:
                values["recommendation"] = recommendation

            if decision:
                values["decision_date"] = fields.Date.context_today(
                    review
                )

            if approved:
                values["approved_by_id"] = review.env.user.id

            review.write(values)

            if message:
                review.message_post(body=message)

    def _close_activities(self):
        """
        Remove all pending activities.
        """

        for review in self:
            if review.activity_ids:
                review.activity_ids.unlink()

    # ---------------------------------------------------------
    # ORM Overrides
    # ---------------------------------------------------------

    def copy(self, default=None):

        default = dict(default or {})

        default.update({
            "review_number": "New",
            "status": "draft",
            "recommendation": "pending",
            "approved_by_id": False,
            "decision_date": False,
            "calendar_event_id": False,
        })

        return super().copy(default)

    def unlink(self):

        for review in self:

            if review.status not in ("draft", "returned"):
                raise ValidationError(
                    _(
                        "Only Draft or Returned reviews "
                        "can be deleted."
                    )
                )

            if review.calendar_event_id:
                review.calendar_event_id.unlink()

        return super().unlink()

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    def name_get(self):

        result = []

        for review in self:

            name = "%s - %s" % (
                review.review_number,
                review.applicant_id.name,
            )

            result.append(
                (
                    review.id,
                    name,
                )
            )

        return result

    # ---------------------------------------------------------
    # Scheduled Utilities
    # ---------------------------------------------------------

    @api.model
    def cron_close_completed_reviews(self):
        """
        Optional maintenance job.

        Archive approved/rejected reviews
        older than one year.
        """

        one_year = fields.Date.today() - timedelta(days=365)

        reviews = self.search([
            ("status", "in", ("approved", "rejected")),
            ("decision_date", "<", one_year),
            ("active", "=", True),
        ])

        if reviews:
            reviews.write({
                "active": False,
            })