from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel
from odoo.addons.datamodel.fields import NestedModel


class WarehouseInfo(Datamodel):
    _name = "warehouse.search.param"

    id = fields.Integer(required=False, allow_none=True)
    row = fields.String(required=False, allow_none=True)
    bay = fields.String(required=False, allow_none=True)
