from odoo import api, fields, models, _


class PatientTag(models.Model):
    _name = "patient.tag"
    _description = "Patient Tag"

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default=True)
    color = fields.Integer(string="Color")
    color_2 = fields.Char(string="Color 2")
    sequence = fields.Integer(string="Sequence")



    # active is added because it's checking in archive as well
    _sql_constraints = [
        ('unique_tag_name', 'unique (name, active)', 'Tag Name must be unique.'),
        ('check_tag_sequence', 'check (sequence > 0)', 'Sequence must be positive integer.')
    ]

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        print('default: ', default)
        if 'name' not in default:
            default['name'] = _("%s (copy)") % (self.name)
        if 'active' not in default:
            default['active'] = False  # Set the copied record to be initially inactive
        return super(PatientTag, self).copy(default=default)
