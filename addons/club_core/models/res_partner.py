from . import res_partnerfrom odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_club_member = fields.Boolean(
        string="Is Club Member",
        default=False,
        help="Flags this contact as a club member.",
    )
    membership_number = fields.Char(
        string="Membership Number",
        copy=False,
        index=True,
        help="Unique membership reference.",
    )
    join_date = fields.Date(
        string="Join Date",
    )
    member_type = fields.Selection(
        selection=[
            ('primary', 'Primary'),
            ('dependent', 'Dependent'),
            ('corporate', 'Corporate'),
        ],
        string="Member Type",
        default='primary',
    )
    primary_member_id = fields.Many2one(
        comodel_name='res.partner',
        string="Primary Member",
        index=True,
        domain="[('is_club_member', '=', True), ('id', '!=', id)]",
        help="Groups family members under one primary billing account.",
    )

    _sql_constraints = [
        (
            'membership_number_uniq',
            'unique(membership_number)',
            'The Membership Number must be unique!',
        ),
    ]