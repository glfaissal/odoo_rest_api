from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel
from odoo.addons.datamodel.fields import NestedModel


class ShelfInfo(Datamodel):
    _name = "shelf.info"
    _inherit = "shelf.short.info"

    is_shelf = fields.Boolean(allow_none=True)
    width = fields.Float(allow_none=True)
    height = fields.Float(allow_none=True)
    depth = fields.Float(allow_none=True)
