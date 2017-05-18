# -*- coding: utf-8 -*-
# © 2017 KMEE (http://www.kmee.com.br)
# Luiz Felipe do Divino<luiz.divino@kmee.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime
from openerp import api, models, fields, exceptions, _


class PurchaseContractItensWizard(models.TransientModel):
    _name = "purchase.contract.itens.wizard"

    name = fields.Char(string="Name", required=True)
    product_id = fields.Many2one(
        comodel_name="product.product", string="Product", required=True
    )
    price = fields.Float(string="Price", required=True)
    quantity = fields.Float(string="Quantity", required=True)
    contract_id = fields.Many2one(
        comodel_name="account.analytic.account",
        string="Contract",
        required=True
    )

    @api.multi
    def create_purchase_contract_item(self):
        vals = {
            'name': self.name,
            'product_id': self.product_id.id,
            'price': self.price,
            'quantity': self.quantity,
            'contract_id': self.contract_id.id
        }
        self.env['contract.purchase.itens'].create(vals)
        return {'type': 'ir.actions.act_window_close'}
