# -*- coding: utf-8 -*-



from odoo import api, fields, models, tools,_
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError

class TransportBill(models.Model):
    _name = "transport.bill"
    _description = 'Transport Bill'
    
   
    bill_no = fields.Char("Bill No", required=True, copy=False, index=True,default =lambda self: _('New'))
    transporter_id = fields.Many2one('res.partner', string="Transporter Name", required=True)
    bill_date = fields.Date("Bill Date")
    bill_line_ids = fields.One2many(
        "bill.line", "bill_line_id", "Bill Lines")
    ref_no = fields.Char("Ref No", size=64)
    ref_date = fields.Date("Ref Date")
    amount_total1 = fields.Float(
        compute='_compute_amount_total',
        string='Total', store=True)
    
   
    amount = fields.Float(
        'Amount',default=0.0,digits = (12,2), compute='_amount_all')
    
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
                        'amount': temp,
                    })
            else:
                self.amount = 0         
    
    ## Auto sequence
    @api.model
    def create (self,vals):
        if vals:
            vals['bill_no'] = self.env['ir.sequence'].next_by_code('transport.bill') or _('New')
        return super(TransportBill,self).create(vals)
    
    ## confrim button
    def action_confirm(self):
        r = []
        obj = []
        print ('start')
        if  self.lr_no:
            res = self.env['vehicle.status'].search([('g_lr_no', '=' , self.lr_no),('incoterm_id', '=' , self.incoterm_id.name),('freight_term','=','Paid')])
            for i in res:
                print(i.delivery_order.name)
                data = { 'picking_id':i.delivery_order.id,
                         'picking_date':i.transport_date,
                         'supplier_id':i.delivery_order.partner_id.id,
                         'vehicle_id': i.id,                                             
                       }   
                obj = [(0,0,data)]
                #print(i.vehicle_id.name)
                self.write({'state': 'ready','receipt_line_ids': obj})  
        

        
class ReceiptLines(models.Model):
    _name = "bill.line"
    _description = 'Receipt Lines'
    
    bill_line_id = fields.Many2one('transport.bill','Transport Bill')
    picking_id = fields.Many2one('stock.picking',"GRIN No.")
    picking_date = fields.Date("GRIN Date")
    supplier_id = fields.Many2one('res.partner', string="Supplier Name")
    lr_no = fields.Char("LR No", size=64)
    lr_amt = fields.Float('LR Amount',default=0.0)
    tax_amount = fields.Float(compute='_compute_tax_amount')
    tax_ids = fields.Many2many(
        'account.tax', string='Taxes',
        domain='[("type_tax_use", "=", "purchase")]')
    
    other_charge = fields.Float(
        'Other Charge',default=0.0)
    
    amount = fields.Float(
        'Amount',default=0.0,digits = (12,2), compute='_compute_amount_total')
    vehicle_id = fields.Many2one('vehicle.status', 'Vehicle')
    
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

                
    
    @api.depends('lr_amt', 'tax_ids','other_charge')
    def _compute_amount_total(self):
        for rec in self:
            rec.amount = rec.lr_amt + rec.tax_amount + rec.other_charge   
           
    
    @api.depends('lr_amt', 'tax_ids','other_charge')
    def _compute_tax_amount(self):
        for rec in self:
            taxes = rec.tax_ids.compute_all(
                rec.lr_amt
                )
            if taxes['taxes']:
                for tax in taxes['taxes']:
                    rec.tax_amount += tax['amount']
            else:
                rec.tax_amount = 0.0
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
    
