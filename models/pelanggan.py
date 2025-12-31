from odoo import models, fields, api



class CdnPelanggan(models.Model):
    _name = 'cdn.pelanggan'
    _description = 'Cdn Pelanggan'
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one(comodel_name='res.partner', required=True, ondelete='cascade', string='Partner')

