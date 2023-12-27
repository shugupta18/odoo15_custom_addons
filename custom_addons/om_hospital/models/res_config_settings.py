from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # 'config_parameter' will create an entry in ir.config_parameter (Technical > System Parameters)
    # if you delete system parameter from UI, make sure to delete the External identifier for it as well
    cancel_days = fields.Integer(string="Cancel Days", config_parameter='om_hospital.cancel_day')
