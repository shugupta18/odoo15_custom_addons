from datetime import date
from odoo import api, fields, models

class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", tracking=True)
    date_of_birth = fields.Date(string="Date of Birth")
    age = fields.Integer(string="Age", compute='_compute_age')
    ref = fields.Char(string="Reference")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string="Gender", default='male')
    # active field is added to enable Archive / Unarchive feature
    active = fields.Boolean(string="Active", default=True)
    appointment_id = fields.Many2one(comodel_name='hospital.appointment', string='Appointments')


    # here self represents recordset not the instance (coming from odoo compute function)
    @api.depends('date_of_birth')
    def _compute_age(self):
        today = date.today()
        for record in self:
            if record.date_of_birth:
                record.age = today.year - record.date_of_birth.year
            # else is required in the compute function otherwise will give error
            else:
                record.age = 0
