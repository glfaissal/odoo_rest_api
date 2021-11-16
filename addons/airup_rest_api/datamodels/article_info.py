# Copyright 2019 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel
from odoo.addons.datamodel.fields import NestedModel


class ArticleInfo(Datamodel):
    _name = "article.info"
    _inherit = "article.short.info"

    name = fields.String(required=False, allow_none=True)
    description = fields.String(required=False, allow_none=True)
#    article_type = fields.String(required=True, allow_none=False)
#    categ_id = fields.Integer(required=True, allow_none=False)


class ArticleUpdate(Datamodel):
    _name = "article.update"

    name = fields.String(required=False, allow_none=True)
    description = fields.String(required=False, allow_none=True)
