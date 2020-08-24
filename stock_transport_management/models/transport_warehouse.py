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


class VehicleSaleOrder(models.Model):
    _inherit = 'stock.picking'

    transportation_name = fields.Char(string="Transportation Via", compute="get_transportation")
    no_parcels = fields.Integer(string="No Of Parcels")
    transportation_details = fields.One2many('vehicle.status', compute='fetch_details', string="Transportation Details")

    #@api.multi
    def get_transportation(self):
        res = self.env['purchase.order'].search([('name', '=', self.purchase_id.name)])
        self.transportation_name = res.transportation_name.name
        order = self.env['vehicle.status'].search([('purchase_order', '=', self.purchase_id.name)])
        if not order and self.transportation_name:
            vals = {'name': self.transportation_name,
                    'no_parcels': self.no_parcels,
                    'g_lr_no': self.purchase_id.g_lr_no,
                    'g_lr_date':self.purchase_id.g_lr_date,
                    'vehicle_no': self.purchase_id.vehicle_no,
                    'purchase_order': self.purchase_id.name,
                    'delivery_order': self.name,
                    'transport_date': self.scheduled_date,
                    #'uom_id': self.product_uom.name,
                    #'warehouse_id' : self.warehouse_id.id, 
                    }
            obj = self.env['vehicle.status'].create(vals)
            return obj

    @api.onchange('no_parcels')
    def get_parcel(self):
        order = self.env['vehicle.status'].search([('purchase_order', '=', self.purchase_id.name)])
        vals = {'no_parcels': self.no_parcels}
        order.write(vals)

    #@api.multi
    def fetch_details(self):
        order = self.env['vehicle.status'].search([('purchase_order', '=', self.purchase_id.name)])
        self.transportation_details = order
    
    
