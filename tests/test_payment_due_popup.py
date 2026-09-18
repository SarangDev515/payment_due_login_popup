# -*- coding: utf-8 -*-

from datetime import timedelta

from odoo import fields
from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class TestPaymentDuePopup(AccountTestInvoicingCommon):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        today = fields.Date.today()
        cls.due_sale = cls._create_invoice(
            move_type='out_invoice',
            invoice_date=today - timedelta(days=10),
            invoice_date_due=today - timedelta(days=1),
            post=True,
        )
        cls.due_purchase = cls._create_invoice(
            move_type='in_invoice',
            invoice_date=today - timedelta(days=10),
            invoice_date_due=today,
            post=True,
        )
        cls.future_sale = cls._create_invoice(
            move_type='out_invoice',
            invoice_date=today,
            invoice_date_due=today + timedelta(days=10),
            post=True,
        )

    def test_due_payment_popup_returns_only_due_sales_and_purchases(self):
        data = self.env['account.move'].get_due_payment_popup_data()

        sales_ids = {item['id'] for item in data['sales']}
        purchase_ids = {item['id'] for item in data['purchases']}

        self.assertIn(self.due_sale.id, sales_ids)
        self.assertIn(self.due_purchase.id, purchase_ids)
        self.assertNotIn(self.future_sale.id, sales_ids)
        self.assertEqual(data['total_count'], len(data['sales']) + len(data['purchases']))
