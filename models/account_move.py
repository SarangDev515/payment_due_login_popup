# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.tools import format_amount, format_date


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def get_due_payment_popup_data(self):
        """Return due customer invoices and vendor bills for the current user.

        The search intentionally uses the current user's environment without
        sudo(), so normal accounting access rights, record rules, and allowed
        companies continue to apply.
        """
        today = fields.Date.context_today(self)
        due_domain = [
            ('state', '=', 'posted'),
            ('move_type', 'in', ('out_invoice', 'in_invoice')),
            ('payment_state', 'in', ('not_paid', 'partial', 'in_payment', 'blocked')),
            ('amount_residual', '>', 0),
            ('invoice_date_due', '!=', False),
            ('invoice_date_due', '<=', today),
        ]
        moves = self.search(
            due_domain,
            order='invoice_date_due asc, move_type asc, id asc',
        )

        payment_state_labels = {
            'not_paid': _('Not Paid'),
            'partial': _('Partially Paid'),
            'in_payment': _('In Payment'),
            'blocked': _('Blocked'),
        }
        sales = []
        purchases = []

        for move in moves:
            item = {
                'id': move.id,
                'number': move.name or move.ref or _('[No Number]'),
                'partner': move.partner_id.display_name or _('[No Partner]'),
                'due_date': format_date(self.env, move.invoice_date_due),
                'amount_due': format_amount(self.env, move.amount_residual, move.currency_id),
                'company': move.company_id.display_name,
                'payment_state': move.payment_state,
                'payment_state_label': payment_state_labels.get(
                    move.payment_state,
                    move.payment_state,
                ),
            }
            if move.move_type == 'out_invoice':
                item['type'] = 'sale'
                item['type_label'] = _('Sales Invoice')
                sales.append(item)
            else:
                item['type'] = 'purchase'
                item['type_label'] = _('Purchase Bill')
                purchases.append(item)

        return {
            'sales': sales,
            'purchases': purchases,
            'total_count': len(sales) + len(purchases),
        }
