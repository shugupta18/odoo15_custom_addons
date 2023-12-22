from odoo import api, fields, models


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _description = "Hospital Appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'ref'

    # Adding Many2one field
    patient_id = fields.Many2one(comodel_name="hospital.patient", string="Patient")
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

    # # this is a class level method
    # @api.model
    # def create(self, vals):
    #     vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
    #     super(HospitalAppointment, self).create(vals)
    #
    # # this is a class instance level method
    # def write(self, vals):
    #     if not self.ref and not vals.get('ref'):
    #         vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
    #     super(HospitalAppointment, self).write(vals)

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.ref = self.patient_id.ref
        return

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
            rec.state = 'in_consultation'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        print('cancel', self)
        action = self.env.ref('om_hospital.action_cancel_appointment').read()[0]
        for rec in self:
            rec.state = 'cancelled'
        return action


class AppointmentPharmacyLines(models.Model):
    _name = "appointment.pharmacy.lines"
    _description = "Appointment Pharmacy Lines"

    product_id = fields.Many2one(comodel_name='product.product', required=True)
    price_unit = fields.Float(related='product_id.list_price')
    qty = fields.Integer(string='Quantity', default=1)

    appointment_id = fields.Many2one(comodel_name='hospital.appointment', string='Appointment')
