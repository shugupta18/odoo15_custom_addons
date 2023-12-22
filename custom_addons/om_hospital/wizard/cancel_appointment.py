import datetime
from odoo import api, fields, models


class CancelAppointmentWizard(models.TransientModel):
    _name = "cancel.appointment.wizard"
    _description = "Cancel Appointment Wizard"

    @api.model
    def default_get(self, fields_list):
        res = super(CancelAppointmentWizard, self).default_get(fields_list)
        res['date_cancel'] = datetime.date.today()
        return res

    appointment_id = fields.Many2one(comodel_name='hospital.appointment', string="Appointment")
    reason = fields.Text(string="Reason")
    date_cancel = fields.Date(string="Cancellation Date")

    def action_cancel(self):
        print('cancel appointment clicked!')
        return
