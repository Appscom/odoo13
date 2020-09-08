# -*- coding: utf-8 -*-



from odoo import api, fields, models, tools,_
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError

class TransportReceipt(models.Model):
    _name = "transport.receipt"
    _description = 'Transport Receipt'
    
    name = fields.Char("Sequence Number", required=True, copy=False, index=True,default =lambda self: _('New'))
    lr_no = fields.Char("LR No", size=64)
    transporter_id = fields.Many2one('res.partner', string="Transporter Name", required=True)
    lr_date = fields.Date("Entry Date")
    incoterm_id = fields.Many2one('account.incoterms', "Mode of Transport",readonly=False)
    paid = fields.Boolean(default=True, string = 'Paid', required=True)
    
    receipt_line_ids = fields.One2many(
        "receipt.line", "receipt_line_id", "Receipt Lines")
    
    lr_charge = fields.Float(
        'LR Charge',default=0.0)
    loading_unloading_charge = fields.Float(
        'Loading/Unloading Charge',default=0.0)
    other_charge = fields.Float(
        'Other Charge',default=0.0)
    amount = fields.Float(
        'Amount',default=0.0,digits = (12,2), compute='_amount_all')
    reason = fields.Text('Reason')
    state = fields.Selection(
        [('draft', 'Draft'),
         ('ready', 'Confirm')],
        string='State', readonly=True, default='draft',
        track_visibility='onchange')

    ##mode and transporter name onchange
   # def get_value(self):
    #     if self.lr_no:
     #        res = self.env['vehicle.status'].search(['g_lr_no', '=' , self.lr_no]) 
      #       self.incoterm_id = res.incoterm_id
       #  else:
        #     self.incoterm_id
            
    
    ##total amount
    def _amount_all(self):
        for rec in self:
            temp = 0.0
            if rec.receipt_line_ids:
                for line in rec.receipt_line_ids:
                    if line.freight > 0:
                        temp += line.freight
                    else:
                        temp=0
                
                    rec.update({
                        'amount': temp + rec.lr_charge + rec.loading_unloading_charge + rec.other_charge,
                    })
            else:
                self.amount = 0         
    
    ## Auto sequence
    @api.model
    def create (self,vals):
        if vals:
            vals['name'] = self.env['ir.sequence'].next_by_code('transport.receipt') or _('New')
        return super(TransportReceipt,self).create(vals)
    
    ## confrim button
    def action_confirm(self):
        r = []
        obj = []
        print ('start')
        if  self.lr_no:
            res = self.env['vehicle.status'].search([('g_lr_no', '=' , self.lr_no),('incoterm_id', '=' , self.incoterm_id.name),('freight_term','=','Paid'),('delivery_order.state', '!=' , 'cancel'),('delivery_order.state', '!=' , 'done')])
            for i in res:
                print(i.delivery_order.name)
                data = { 'picking_id':i.delivery_order.id,
                         'picking_date':i.transport_date,
                         'supplier_id':i.delivery_order.partner_id.id,
                         'vehicle_id': i.id,
                         'do_load_weight':i.load_weight,
                         'do_tar_weight':i.tane_weight,
                         'do_net_weight':i.net_weight,
                       }   
                obj = [(0,0,data)]
                #print(i.vehicle_id.name)
                self.write({'state': 'ready','receipt_line_ids': obj})  
        

        
class ReceiptLines(models.Model):
    _name = "receipt.line"
    _description = 'Receipt Lines'
    
    receipt_line_id = fields.Many2one('transport.receipt','Transport Receipt')
    picking_id = fields.Many2one('stock.picking',"GRIN No.")
    picking_date = fields.Date("GRIN Date")
    supplier_id = fields.Many2one('res.partner', string="Supplier Name")
    load_weight = fields.Float('Load Weight',default=0.0)
    tane_weight = fields.Float('Tane Weight',default=0.0)
    net_weight = fields.Float('Net Weight',default=0.0)
    rate  = fields.Float('Rate per Kg',default=0.0,compute='get_rate',digits = (12,2))
    freight = fields.Float('Freight',default=0.0,compute='get_freight',digits = (12,2))
    vehicle_id = fields.Many2one('vehicle.status', 'Vehicle')
    


   # _sql_constraints = [
    #    ('stock_uniq',
     #   'unique(picking_id)',
      #  'You can not create two Receipt point for same GRIN ! and Receipt was generated for GRN'),
    #]



    ##get rate from vehicle.status
    def get_rate(self):
        #self.ensure_one()
        for i in self:
            print(i.vehicle_id)
            if i.vehicle_id.rate > 0:
                i.rate = i.vehicle_id.rate 
            else:
                i.rate = 0
    
    ##calc freight
    def get_freight(self):
        for i in self:
            if (i.rate and i.net_weight) > 0:
                print(i.net_weight , i.rate)
                i.freight = i.net_weight * i.rate
            else:
                i.freight = 0
            
    

