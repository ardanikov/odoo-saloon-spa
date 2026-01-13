from odoo import models, fields, api
from odoo.exceptions import UserError

class CdnAppointmentHeader(models.Model):
    _name = 'cdn.appointment'
    _description = 'Cdn Appointment'

    name = fields.Char(string='No. Appointment')
    pelanggan_id = fields.Many2one(comodel_name='res.partner', domain=[('is_pelanggan', '=', True)], required=True, ondelete='cascade', string='Pelanggan')
    tanggal = fields.Date(string='Tanggal')
    # cabang_id = fields.Many2one(comodel_name='stock.warehouse', string='Cabang')
    status = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm')], string='Status', default='draft')
    invoice_id = fields.Many2one(comodel_name='account.move', ondelete='cascade', string='Invoice', readonly=True)
    payment_state = fields.Selection(related='invoice_id.payment_state', string="Status Pembayaran")
    picking_id = fields.Many2one(comodel_name='stock.picking', string='Pengambilan Barang', readonly=True)
    sale_order_id = fields.Many2one(comodel_name='sale.order', string='Sale Order', readonly=True)
    appointment_line_ids = fields.One2many(comodel_name='cdn.appointment.line', inverse_name='appointment_id', string='Appointment Lines')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    amount_total = fields.Monetary(string='Total', compute='_compute_amount_total', currency_field='currency_id', store=True)
    terapis_id = fields.Many2one(comodel_name='cdn.terapis', string='Terapis')
    spesialis_id = fields.Many2one(comodel_name='cdn.spesialis', string='Spesialis')
    

    @api.onchange('terapis_id')
    def _onchange_terapis_id(self):
        if self.terapis_id:
            self.spesialis_id = self.terapis_id.spesialis_ids
    

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('cdn.appointment.name.sequence')
        return super(CdnAppointmentHeader, self).create(vals)

    @api.depends('appointment_line_ids.price_total')
    def _compute_amount_total(self):
        for record in self:
            record.amount_total = sum(line.price_total for line in record.appointment_line_ids)


    def action_confirm(self):
        for record in self:
            if record.status == 'draft':
                record.status = 'confirm'
                

    def action_reset(self):
        for record in self:
            record.status = 'draft'

    def action_create_invoice(self):
        for record in self:
            sale_vals = {
                'partner_id': record.pelanggan_id.id,
                'date_order': record.tanggal,
            }
            sale_order = self.env['sale.order'].with_context(
                # warehouse_id=record.cabang_id.id,
                # company_id=record.cabang_id.company_id.id
            ).create(sale_vals)
            
            for line in record.appointment_line_ids:
                self.env['sale.order.line'].create({
                    'order_id': sale_order.id,
                    'product_id': line.produk_id.id,
                    'product_uom_qty': line.product_quantity,
                    'price_unit': line.price_unit,
                })
            
            sale_order.action_confirm()
            
        
            invoice = sale_order._create_invoices()
            invoice.action_post()
            
      
            record.sale_order_id = sale_order.id
            record.invoice_id = invoice.id
            if sale_order.picking_ids:
                record.picking_id = sale_order.picking_ids[0].id


    def action_confirm_bayar(self):
        self.ensure_one()
        if not self.invoice_id:
            raise UserError("Tagihan belum dibuat.")
        return self.invoice_id.action_register_payment()

class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    def action_create_payments(self):
        res = super(AccountPaymentRegister, self).action_create_payments()
        
        # The invoices are in self.line_ids.move_id
        invoices = self.line_ids.move_id
        for invoice in invoices:
            if invoice.payment_state in ('paid', 'in_payment'):
                sale_orders = invoice.invoice_line_ids.mapped('sale_line_ids.order_id')
                for sale in sale_orders:
                    for picking in sale.picking_ids:
                        if picking.state not in ('done', 'cancel'):
                            for line in picking.move_ids_without_package:
                                line.quantity = line.product_uom_qty
                            picking.button_validate()
        return res




class CdnAppointmentLine(models.Model):
    _name = 'cdn.appointment.line'
    _description = 'Cdn Appointment Line'

    appointment_id = fields.Many2one(comodel_name='cdn.appointment', required=True, ondelete='cascade', string='Appointment')
    # cabang_id = fields.Many2one(related='appointment_id.cabang_id', string='Cabang')
    produk_id = fields.Many2one(comodel_name='product.product', required=True, ondelete='cascade', domain=[('is_spa_product', '=', True)], string='Produk')
    product_quantity = fields.Integer(string='Kuantitas', default=1, required=True)
    currency_id = fields.Many2one(related='appointment_id.currency_id', depends=['appointment_id.currency_id'], store=True, string='Currency')
    price_unit = fields.Float(string='Harga', required=True, digits='Harga')
    price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', store=True, currency_field='currency_id')
    price_total = fields.Monetary(compute='_compute_amount', string='Total', store=True, currency_field='currency_id')

    @api.depends('product_quantity', 'price_unit')
    def _compute_amount(self):
        for line in self:
            price = line.price_unit * line.product_quantity
            line.update({
                'price_subtotal': price,
                'price_total': price,
            })

    @api.onchange('produk_id')
    def _onchange_produk_id(self):
        if self.produk_id:
            self.price_unit = self.produk_id.lst_price
