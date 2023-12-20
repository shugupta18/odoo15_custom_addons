from odoo import api, fields, models

class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _description = "Hospital Appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'ref'

    # Adding Many2one field
    patient_id = fields.Many2one(comodel_name="hospital.patient", string="Patient")

    # Adding Date and Datetime fields with default values
    appointment_datetime = fields.Datetime(string="Appointment Time", default=fields.Datetime.now)
    booking_date = fields.Date(string="Booking Date", default=fields.Date.context_today)

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

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.ref = self.patient_id.ref

    def func_test(self):
        print("Object button pressed!")
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Click successful',
                'type': 'rainbow_man'
            }
        }
