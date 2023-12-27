import random

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _description = "Hospital Appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'ref'
    _order = 'id desc'

    # required for showing currency
    company_id = fields.Many2one(comodel_name='res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one(comodel_name='res.currency', related='company_id.currency_id')

    # Adding Many2one field
    # ondelete='restrict' OR ondelete='cascade'
    patient_id = fields.Many2one(comodel_name="hospital.patient", string="Patient", ondelete='cascade')
    doctor_id = fields.Many2one(comodel_name='res.users', string='Doctor')

    # Adding One2many fields (model, field with Many2one relation in pharmacy model , string)
    pharmacy_line_ids = fields.One2many('appointment.pharmacy.lines', 'appointment_id', string='Pharmacy lines')

    # Adding Date and Datetime fields with default values
    appointment_datetime = fields.Datetime(string="Appointment Time", default=fields.Datetime.now)
    booking_date = fields.Date(string="Booking Date", default=fields.Date.context_today)

    # field added just to test hiding One2many column based on Parent
    # Record
    hide_sales_price = fields.Boolean(string="Hide Sales Price")

    # Add a related field
    gender = fields.Selection(related='patient_id.gender', readonly=True)

    # ref field changes based onChange function
    ref = fields.Char(string='Reference', help='Reference of the patient record')

    # it is a html field
    prescription = fields.Html(string='Prescription')

    # priority widget
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string='Priority')

    # status bar widget
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_consultation', 'In Consultation'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string="Status", default='draft', required=True)

    # add an image field for patient image (in avatar mode)
    image = fields.Image(string="Image")

    operation_id = fields.Many2one(comodel_name='hospital.operation', string='Operation')

    progress = fields.Integer(string='Progress', compute='_compute_progress')
    duration = fields.Float(string="Duration")

    def func_test(self):
        print("Object button pressed!")
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Click successful',
                'type': 'rainbow_man'
            }
        }

    # self is a loop representing recordset in odoo,
    # we could pass a list for which we want states to be cancelled

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_in_consultation(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'in_consultation'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        action = self.env.ref('om_hospital.action_cancel_appointment').read()[0]
        for rec in self:
            rec.state = 'cancelled'
        return action

    # this is a class level method
    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        return super(HospitalAppointment, self).create(vals)

    # this is a class instance level method
    def write(self, vals):
        if not self.ref and not vals.get('ref'):
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        super(HospitalAppointment, self).write(vals)

    def unlink(self):
        for record in self:
            if record.state != 'draft':
                raise ValidationError(_("Only appointments in 'draft' state can be deleted"))
        return super(HospitalAppointment, self).unlink()

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.ref = self.patient_id.ref

    @api.depends('state')
    def _compute_progress(self):
        for record in self:
            if record.state == 'draft':
                progress = random.randrange(0, 25)
            elif record.state == 'in_consultation':
                progress = random.randrange(25, 75)
            elif record.state == 'done':
                progress = 100
            else:
                progress = 0
            record.progress = progress


class AppointmentPharmacyLines(models.Model):
    _name = "appointment.pharmacy.lines"
    _description = "Appointment Pharmacy Lines"

    product_id = fields.Many2one(comodel_name='product.product', required=True)
    price_unit = fields.Float(related='product_id.list_price')
    qty = fields.Integer(string='Quantity', default=1)
    appointment_id = fields.Many2one(comodel_name='hospital.appointment', string='Appointment')
    company_currency_id = fields.Many2one(comodel_name='res.currency', related='appointment_id.currency_id')
    price_subtotal = fields.Monetary(string='Subtotal', currency_field='company_currency_id', compute='_compute_price_subtotal')

    @api.depends('price_unit', 'qty')
    def _compute_price_subtotal(self):
        for record in self:
            record.price_subtotal = record.price_unit * record.qty
