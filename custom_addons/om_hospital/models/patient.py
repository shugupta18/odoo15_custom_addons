from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


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
    # add a Many2many field
    tag_ids = fields.Many2many('patient.tag', string="Tags")
    # stored compute Field
    appointment_count = fields.Integer(string="Appointment Count", compute='_compute_appointment_count', store=True)
    appointment_ids = fields.One2many(comodel_name='hospital.appointment', inverse_name='patient_id', string="Appointments")

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for record in self:
            record.appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', record.id)])

    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for record in self:
            if record.date_of_birth and record.date_of_birth > fields.Date.today():
                raise ValidationError(_('The entered date of birth is not acceptable!'))

    # this is a class level method
    @api.model
    def create(self, vals):
        # vals['ref'] = 'HP0TEST'
        vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).create(vals)

    # this is a class instance level method
    def write(self, vals):
        # print('print self: ', self, 'print self.ref: ', self.ref, 'vals: ',  vals)
        if not self.ref and not vals.get('ref'):
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        super(HospitalPatient, self).write(vals)

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

    def name_get(self):
        return [(record.id, f"[{record.ref}]: {record.name}") for record in self]
