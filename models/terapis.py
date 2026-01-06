from odoo import models, fields, api

class CdnTerapis(models.Model):
    _name = 'cdn.terapis'
    _description = 'Terapis'

    kode = fields.Char(string='Kode Terapis', readonly=True, copy=False, default='New')
    name = fields.Char(string='Nama Terapis', required=True)

    phone = fields.Char(string='No. HP')
    email = fields.Char(string='Email')

    gender = fields.Selection([
        ('male', 'Laki-laki'),
        ('female', 'Perempuan'),
    ], string='Jenis Kelamin')

    aktif = fields.Boolean(string='Aktif', default=True)
    note = fields.Text(string='Catatan')

    spesialis_ids = fields.One2many(
        'cdn.spesialis',
        'terapis_id',
        string='Spesialis'
    )
    
    @api.model
    def create(self, vals):
        if vals.get('kode', 'New') == 'New':
            vals['kode'] = self.env['ir.sequence'].next_by_code(
                'cdn.terapis'
            ) or 'New'
        return super().create(vals)