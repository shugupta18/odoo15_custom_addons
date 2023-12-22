from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    confirmed_user_id = fields.Many2one(comodel_name='res.users', string="Confirmed User")

    def action_confirm(self):
        super(SaleOrder, self).action_confirm()
        # gives current user id
        self.confirmed_user_id = self.env.user.id
