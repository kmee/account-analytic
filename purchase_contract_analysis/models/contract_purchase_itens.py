# -*- coding: utf-8 -*-
# © 2017 KMEE (http://www.kmee.com.br)
# Luiz Felipe do Divino<luiz.divino@kmee.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models, fields


class ContractPurchaseItens(models.Model):
    _name = "contract.purchase.itens"

    @api.multi
    def _get_purchase_orders_of_the_contract(self, record):
        sale_order_obj = self.env['purchase.order']
        return sale_order_obj.search(
            [
                ('project_id', '=', record.contract_id.id)
            ]
        )

    @api.multi
    def _get_purchase_lines_of_product(self, product_id, sale_order_ids):
        sale_order_line_obj = self.env['purchase.order.line']
        return sale_order_line_obj.search(
            [
                ('product_id', '=', product_id),
                ('order_id', 'in', sale_order_ids)
            ]
        )

    def _get_purchase_invoice_values(self, purchase_order_ids):
        purchase_order_names = []
        for purchase_order in purchase_order_ids:
            if purchase_order.name not in purchase_order_names:
                purchase_order_names.append(purchase_order.name)
        purchase_invoices = self.env['account.invoice'].search(
            [
                ('origin', 'in', purchase_order_names)
            ]
        )
        total = 0.0
        for purchase_invoice in purchase_invoices:
            for line in purchase_invoice.invoice_line:
                if line.product_id.id == self.product_id.id:
                    total += line.price_subtotal
        self.invoiced = total

    def _get_purchase_order_values(self, purchase_order_ids):
        purchase_line_ids = \
            self._get_purchase_lines_of_product(
                self.product_id.id, purchase_order_ids.ids
            )
        total = 0.0
        qty = 0.0
        for line in purchase_line_ids:
            total += line.price_subtotal
            qty += line.product_qty

        self.invoiced_qty = qty
        self.to_invoice = total - self.invoiced

    @api.depends('product_id', 'contract_id', 'price', 'quantity')
    @api.multi
    def _compute_to_invoice_amount(self):
        for record in self:
            if record.contract_id:
                purchase_order_ids = \
                    self._get_purchase_orders_of_the_contract(record)
                record._get_purchase_invoice_values(purchase_order_ids)
                record._get_purchase_order_values(purchase_order_ids)

                record.remaining_qty = record.quantity - record.invoiced_qty
                record.remaining = record.remaining_qty*record.price
                record.expected = \
                    record.price * record.remaining_qty + record.invoiced + \
                    record.to_invoice

    @api.onchange('product_id')
    def _compute_price(self):
        self.price = self.product_id.lst_price

    name = fields.Char(string="Name", required=True)
    product_id = fields.Many2one(
        comodel_name="product.product", string="Product", required=True
    )
    price = fields.Float(string="Price", required=True)
    quantity = fields.Float(string="Quantity", required=True)
    expected = fields.Float(
        string="Expected",
        compute=_compute_to_invoice_amount,
        store=True
    )
    invoiced = fields.Float(
        string="Invoiced",
        compute=_compute_to_invoice_amount
    )
    invoiced_qty = fields.Float(
        string="Invoiced Qty",
        compute=_compute_to_invoice_amount,
    )
    to_invoice = fields.Float(
        string="To Invoice",
        compute=_compute_to_invoice_amount
    )
    remaining_qty = fields.Float(
        string="Remaining Qty",
        compute=_compute_to_invoice_amount
    )
    contract_id = fields.Many2one(
        comodel_name="account.analytic.account",
        string="Contract",
    )
    date_end = fields.Date(
        string="Final Date"
    )
    remaining = fields.Float(
        string="Remaining",
        compute=_compute_to_invoice_amount
    )
