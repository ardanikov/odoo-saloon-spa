from odoo import models, fields, api



class ResPartner(models.Model):
    _inherit = 'res.partner'

    jenis_kelamin = fields.Selection(selection=[('laki-laki', 'Laki-Laki'), ('perempuan', 'Perempuan')], string="Jenis Kelamin")
    is_pelanggan = fields.Boolean(string='Adalah Pelanggan', default=False)
    is_terapis = fields.Boolean(string='Adalah Terapis', default=False)
 