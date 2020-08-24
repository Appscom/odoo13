# -*- coding: utf-8 -*-
##############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2017-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Saritha Sahadevan(<https://www.cybrosys.com>)
#    you can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (AGPL v3) along with this program.
#    If not, see <https://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields, api


class VehicleCreation(models.Model):
    _name = 'sale.vehicle'

    name = fields.Char(string="Vehicle Name", required=True)
    freight_term = fields.Selection([('To Pay','To Pay'),('Paid','Paid')],('Freight Term'))
    supplier_id = fields.Many2one('res.partner', string="Supplier Name", required=True)
    vehicle_image = fields.Binary(string='Image', store=True, attachment=True)
    # licence_plate = fields.Char(string="Licence Plate", required=True)
    mob_no = fields.Char(string="Mobile Number")
    vehicle_address = fields.Char(string="Address")
    vehicle_city = fields.Char(string='City')
    vehicle_zip = fields.Char(string='ZIP')
    state_id = fields.Many2one('res.country.state', string='State')
    country_id = fields.Many2one('res.country', string='Country')
    active_available = fields.Boolean(string="Active", default=True)
    transportable_line_ids = fields.One2many(
        'tms.waybill.line', 'waybill_id', string="Transportable")
    amount_total = fields.Float(
        compute='_amount_all',
        string='Total', store=True)
        
    @api.depends('transportable_line_ids.rate')
    def _amount_all(self):
        for rec in self:
            temp = 0.0
            for line in rec.transportable_line_ids:
                if line.rate > 0:
                    temp += line.rate
                
                rec.update({
                    'amount_total': temp,
                })
  
    
class TmsWaybillLine(models.Model):
    _name = 'tms.waybill.line'
    _description = 'Waybill Line'
    
    waybill_id = fields.Many2one(
        'sale.vehicle','WayBill'
        )
    name = fields.Char('Description')
    transportable_uom_id = fields.Many2one(
        'uom.uom', 'Freight Type')
    #product_qty = fields.Float(
        #compute='_compute_transportable_product',
     #   string='Qty')
    product_value = fields.Float(
        #compute='_compute_transportable_product',
        string='LCV Value')
    product_weight = fields.Float(
        #compute='_compute_transportable_product',
        string='LCV Weight')
    lr_charge = fields.Float(
        #compute='_compute_amount_freight',
        string='Freight')
    amount_highway_tolls = fields.Float(
        #compute='_compute_amount_highway_tolls',
        string='Highway Tolls')
    amount_untaxed = fields.Float(
        #compute='_compute_amount_untaxed',
        string='SubTotal', store=True)
    amount_tax = fields.Float(
        #compute='_compute_amount_tax',
        string='Taxes')
    amount_total = fields.Float(
        compute='_compute_amount_total',
        string='Total', store=True)
    rate = fields.Float(
        default=0.0,compute='_compute_rate', string='Rate (Kg)',readonly=False )
    price_subtotal = fields.Float(
        #compute='_compute_amount_line',
        string='Subtotal')
    
    @api.depends()
    def _compute_rate(self):
        for rec in self:
            if (rec.product_value and rec.product_weight) > 0:
                if rec.transportable_uom_id.name == 'LCV':
                    rec.rate = rec.product_value / rec.product_weight
                    #print(rec.rate)
                else:
                    rec.rate
    
    
