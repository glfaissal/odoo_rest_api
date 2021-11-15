from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel
from odoo.addons.datamodel.fields import NestedModel


class WarehouseInfo(Datamodel):
    _name = "warehouse.shorter.info"

    id = fields.Integer(required=False, allow_none=True)
    name = fields.String(required=False, allow_none=True)
    amount = fields.Integer(required=False, allow_none=True)

class WarehouseInfo(Datamodel):
    _name = "warehouse.article.shelfs"

    id = fields.Integer(required=False, allow_none=True)
    name = fields.String(required=False, allow_none=True)
    shelfs = fields.List(NestedModel("shelf.detail.warehouse"), required=False)
    debug = fields.String(required=False, allow_none=True)