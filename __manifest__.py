# -*- coding: utf-8 -*-
{
      'name': 'Payment Due Login Popup',
      'version': '19.0.1.0.0',
      'category': 'Accounting/Accounting',
      'summary': 'Show due customer invoices and vendor bills when users enter Odoo',
      'description': """
      Payment Due Login Popup
      ======================
      Displays a reminder dialog after the Odoo backend is ready when the current user
      has posted customer invoices or vendor bills that are due and still unpaid.

      The data is fetched with the normal user's access rights and allowed companies.
      """,
      'author': 'SARANG T',
      'license': 'LGPL-3',
      'depends': ['account', 'web'],
      'data': [],
      'assets': {
                'web.assets_backend': [
                              'payment_due_login_popup/static/src/xml/payment_due_login_popup.xml',
                              'payment_due_login_popup/static/src/js/payment_due_login_popup.js',
                              'payment_due_login_popup/static/src/scss/payment_due_login_popup.scss',
                ],
      },
      'installable': True,
      'application': False,
      'auto_install': False,
}
