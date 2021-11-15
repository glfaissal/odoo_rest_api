from odoo import fields, models, api

class Shelf(models.Model):
    """Shelf"""

    _description = "Shelf"
    _inherit = "stock.location"

    is_shelf = fields.Boolean('Shelf')
    storage_row  = fields.Many2one('stock.location'
                           'Row',
                            related='location_id',
                            )
    row = fields.Char(string='Row',
                               related='location_id.location_id.name')
    bay = fields.Char(string='Bay',
                               related='location_id.name')
    height = fields.Float(string = "Height", default = 0.0)
    width  = fields.Float(string = "width", default = 0.0) 
    depth  = fields.Float(string = "depth", default = 0.0)
