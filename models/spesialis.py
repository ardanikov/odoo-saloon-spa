from odoo import models, fields

class CdnSpesialis(models.Model):
    _name = 'cdn.spesialis'
    _description = 'Spesialis Terapis'

    terapis_id = fields.Many2one(
        'cdn.terapis',
        ondelete='cascade',
        required=True
    )

    name = fields.Char(string='Nama Spesialis', required=True)
    note = fields.Text(string='Keterangan')