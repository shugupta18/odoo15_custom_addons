from odoo import models, fields, api

class HospitalPatient(models.Model):
    _name = "hospital.appointment"
    _description = "Appointment"

    name = fields.Char(string="Name")
    age = fields.Integer(string="Age")
    ref = fields.Char(string="Reference")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string="Gender")
    active = fields.Boolean(string="Active", default=True)
