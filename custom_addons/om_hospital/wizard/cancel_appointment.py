import datetime
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CancelAppointmentWizard(models.TransientModel):
    _name = "cancel.appointment.wizard"
    _description = "Cancel Appointment Wizard"

    @api.model
    def default_get(self, fields_list):
        res = super(CancelAppointmentWizard, self).default_get(fields_list)
        res['date_cancel'] = datetime.date.today()
        # print('context:', self.env.context)
        if self.env.context.get('active_id'):
            res['appointment_id'] = self.env.context.get('active_id')
        return res

    appointment_id = fields.Many2one(comodel_name='hospital.appointment', string="Appointment",
                                     domain=[('state', '=', 'draft')])
    reason = fields.Text(string="Reason")
    date_cancel = fields.Date(string="Cancellation Date")

    def action_cancel(self):
        print('cancel appointment clicked!')
        if self.appointment_id.booking_date == fields.Date.today():
            raise ValidationError(_("Sorry, cancellation is not allowed on the same day of the booking!"))
        return
