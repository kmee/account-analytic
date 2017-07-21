# -*- coding: utf-8 -*-
# © 2017 KMEE (http://www.kmee.com.br)
# Luiz Felipe do Divino<luiz.divino@kmee.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class PurchaseOrderProrrogacaoEntrega(models.Model):
    _name = 'purchase.order.prorrogacao.entrega'

    motivo = fields.Char(
        string=u'Motivo da Prorrogação',
        required=True
    )
    prazo_entrega_atual = fields.Date(
        string=u'Prazo de Entrega Atual',
        store=True
    )
    novo_prazo_entrega = fields.Date(
        string=u'Novo Prazo de Entrega',
        # required=True
    )

    order_id = fields.Many2one(
        comodel_name='purchase.order',
        ondelete='cascade'
    )

    @api.model
    def create(self, vals):
        alteracao = super(PurchaseOrderProrrogacaoEntrega, self).create(vals)
        alteracao.order_id.prazo_entrega = alteracao.novo_prazo_entrega
        alteracao.data_prorrogacao = fields.Date.today()
        return alteracao