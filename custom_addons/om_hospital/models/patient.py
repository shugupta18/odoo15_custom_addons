from datetime import date
from dateutil import relativedelta
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", tracking=True)
    date_of_birth = fields.Date(string="Date of Birth")
    age = fields.Integer(string="Age", compute='_compute_age', inverse='_inverse_compute_age',
                         search='_search_age')
    ref = fields.Char(string="Reference")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string="Gender", default='male')
    # active field is added to enable Archive / Unarchive feature
    active = fields.Boolean(string="Active", default=True)
    appointment_id = fields.Many2one(comodel_name='hospital.appointment', string='Appointments')
    # add a Many2many field
    tag_ids = fields.Many2many('patient.tag', string="Tags")
    # stored compute Field
    appointment_count = fields.Integer(string="Appointment Count", compute='_compute_appointment_count', store=True)
    appointment_ids = fields.One2many(comodel_name='hospital.appointment', inverse_name='patient_id', string="Appointment Ids")

    parent = fields.Char(string="Parent")
    marital_status = fields.Selection(selection=[('married', 'Married'), ('single', 'Single')], string="Marital Status",
                                      tracking=True)
    partner_name = fields.Char(string="Partner Name")
    is_birthday = fields.Boolean(string='Is Birthday', compute='_compute_is_birthday')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    website = fields.Char(string='Website')

    @api.depends('date_of_birth')
    def _compute_is_birthday(self):
        for record in self:
            is_birthday = False
            if record.date_of_birth:
                today = date.today()
                if today.day == record.date_of_birth.day and today.month == record.date_of_birth.month:
                    is_birthday = True
            record.is_birthday = is_birthday

    @api.ondelete(at_uninstall=False)
    def _check_appointments(self):
        for record in self:
            if record.appointment_ids:
                raise ValidationError(_("You cannot delete patient with appointments!"))

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        # for record in self:
        #     record.appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', record.id)])
        appointment_group = self.env['hospital.appointment'].read_group(
                                domain=[], fields=['patient_id'], groupby=['patient_id'])
        for appointment in appointment_group:
            patient_id = appointment.get('patient_id')[0]
            patient_rec = self.browse(patient_id)
            patient_rec.appointment_count = appointment['patient_id_count']
            self -= patient_rec
        self.appointment_count = 0

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

    @api.depends('age')
    def _inverse_compute_age(self):
        today = date.today()
        for record in self:
            record.date_of_birth = today - relativedelta.relativedelta(years=record.age)

    def _search_age(self, operator, value):
        date_of_birth = date.today() - relativedelta.relativedelta(years=value)
        start_of_year = date_of_birth.replace(day=1, month=1)
        end_of_year = date_of_birth.replace(day=31, month=12)
        return [('date_of_birth', '>=', start_of_year), ('date_of_birth', '<=', end_of_year)]

    def name_get(self):
        return [(record.id, f"[{record.ref}]: {record.name}") for record in self]

    def action_test(self):
        print("Click Me button is clicked!")
        return

    def action_view_appointment(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Appointments'),
            'res_model': 'hospital.appointment',
            'view_mode': 'list,form,calendar,activity',
            'target': 'current',
            'context': {'default_patient_id': self.id},
            'domain': [('patient_id', '=', self.id)]
        }
