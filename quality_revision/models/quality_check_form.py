# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class QualityCheckInherit(models.Model):
    _inherit = "quality.check"
    

    control_point = fields.Char(string='Control Point',readonly=True, compute='_compute_values', store= True)
    quality_point_type = fields.Char(string='Control Point Type',readonly=True, compute='_compute_values', store= True )
    norm = fields.Float(string='Control Point',readonly=True, compute='_compute_values', store= True)
    norm_unit = fields.Char(string='Control Point',readonly=True, compute='_compute_values', store= True)
    tolerance_min = fields.Float(string='Control Point',readonly=True, compute='_compute_values', store= True)
    tolerance_max = fields.Float(string='Control Point', compute='_compute_values', store= True)
    
    @api.depends('point_id')
    def _compute_values(self):
        for i in self:
            i.control_point = i.point_id.name
            i.quality_point_type = i.point_id.test_type_id.name
            i.norm = i.point_id.norm
            i.norm_unit = i.point_id.norm_unit
            i.tolerance_min = i.point_id.tolerance_min
            i.tolerance_max = i.point_id.tolerance_max
        
        
    
    
    
    
    
    
    
    
