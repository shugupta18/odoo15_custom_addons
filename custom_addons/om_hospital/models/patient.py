from odoo import api, fields, models

class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", tracking=True)
    age = fields.Integer(string="Age")
    ref = fields.Char(string="Reference")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string="Gender")
    # active field is added to enable Archive / Unarchive feature
    active = fields.Boolean(string="Active", default=True)
