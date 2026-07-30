{
    'name': 'Club Core',
    'version': '19.0.1.0.0',
    'category': 'Association',
    'summary': 'Core membership base for club management ERP.',
    'description': """
Club Core (Membership Base)
===========================
Extends the default contact system to identify and organize
club members and their dependents.

* Adds club-specific fields to Contacts (res.partner).
* Groups family members under a single primary billing account.
* Contains no billing logic (foundational module).
    """,
    'author': 'Your Company',
    'website': 'https://yourcompany.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'contacts',
    ],
    'data': [
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}