from odoo import models, fields

class CdnSpesialis(models.Model):
    _name = 'cdn.spesialis'
    _description = 'Spesialis Terapis'
    _rec_name = 'name'

    kode = fields.Char(
        string='Kode',
        required=True,
        copy=False
    )

    name = fields.Char(
        string='Nama Spesialis',
        required=True
    )

    kategori = fields.Selection(
        [
            ('salon', 'Salon'),
            ('spa', 'Spa'),
            ('salon_spa', 'Salon & Spa'),
        ],
        string='Kategori',
        required=True,
        default='salon'
    )

    deskripsi = fields.Text(string='Deskripsi')
    note = fields.Text(string='Keterangan')

    aktif = fields.Boolean(
        string='Aktif',
        default=True
    )
