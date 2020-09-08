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

from odoo import models, fields,api,_


class VehicleStatus(models.Model):
    _name = 'vehicle.status'

    name = fields.Many2one('sale.vehicle',string="Transportation Via")
    transport_date = fields.Date(string="Transportation Date")
    no_parcels = fields.Char(string="No of Parcels")
    g_lr_no = fields.Char('LR No', size=64)
    g_lr_date = fields.Date('LR Date')
    vehicle_no = fields.Char('Vehicle No',size=64)
    purchase_order = fields.Char(string='Purchase Order')
    delivery_order = fields.Many2one('stock.picking',string="Po Against Receipt Order")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    ], string='Status', readonly=True, index=True, track_visibility='onchange', default='draft',compute='get_state')
    uom_id = fields.Many2one(
        'uom.uom', 'Unit of Measure ')
    incoterm_id = fields.Many2one('account.incoterms', "Mode of Transport")
    rate  = fields.Float('Rate per Kg',default=0.0,compute='get_rate',copy=True)
    freight_term = fields.Selection([('To Pay','To Pay'),('Paid','Paid')],('Freight Term'),readonly=False)
    
    @api.onchange('name','incoterm_id')
    def get_rate(self):
        val = self.name.transportable_line_ids.search([('incoterm_id', '=' , self.incoterm_id.name)])
        if val:
            for i in val:
                print(i.name)
                if i.lr_rate > 0:
                    self.rate = i.lr_rate
                else:
                    self.rate = i.rate
        else:
            self.rate = 0
            
            
    def get_state(self):
        val = self.delivery_order.state
        if val == 'Done' or val == 'done':
            self.write({'state': 'done'})
        elif val == 'cancel' or val == 'Cancelled':
            self.write({'state': 'cancel'})
        else:
            self.write({'state': 'draft'})
            
            
            
    
#    def action_cancel(self):
#        self.write({'state': 'cancel'})
#        vehicle = self.env['sale.vehicle'].search([('name', '=', self.name)])
#        vals = {'active_available': True}
#        vehicle.write(vals)

#    def action_done(self):
#        self.write({'state': 'done'})
#        vehicle = self.env['sale.vehicle'].search([('name', '=', self.name)])
#        vals = {'active_available': True}
#        vehicle.write(vals)

#    def action_waiting(self):
#        vehicle = self.env['sale.vehicle'].search([('name', '=', self.name)])
#        vals = {'active_available': False}
#        vehicle.write(vals)
#        self.write({'state': 'waiting'})

#   def action_reshedule(self):
#        self.write({'state': 'draft'})
        
