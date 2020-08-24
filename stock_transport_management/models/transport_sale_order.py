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


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"


    transportation_name = fields.Many2one('sale.vehicle', string="Transportation Name",
                                          domain=[('active_available', '=', True)])
    freight_term = fields.Selection([('To Pay','To Pay'),('Paid','Paid')],('Freight Term'))
    g_lr_no = fields.Char('LR No', size=64)
    g_lr_date = fields.Date('LR Date')
    vehicle_no = fields.Char('Vehicle No',size=64)


    @api.onchange('transportation_name')
    def on_change_select(self):
        values = {
            'freight_term': self.transportation_name.freight_term or False, 
        }
        self.update(values)

    

