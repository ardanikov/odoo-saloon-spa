from odoo import models, fields, api


class Cabang(models.Model):
    _name = 'cdn.cabang'
    _description = 'Cabang'

    cabang_id = fields.Many2one(comodel_name='stock.warehouse', string='Cabang')
    
