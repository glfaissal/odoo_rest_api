from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel


class ShelfShortInfo(Datamodel):
    _name = "shelf.short.info"

    id = fields.Integer(required=True, allow_none=False)
    name = fields.String(required=False, allow_none=True)
    row = fields.String(required=False, allow_none=True)
    bay = fields.String(required=False, allow_none=True)


class ShelfShorterInfo(Datamodel):
    _name = "shelf.shorter.info"

    depth = fields.Float(required=False, allow_none=True)

class ShelfDetailWarehouse(Datamodel):
    _name = "shelf.detail.warehouse"

    amount = fields.Integer(required=False, allow_none=True)
    row = fields.String(required=False, allow_none=True)
    bay = fields.String(required=False, allow_none=True)