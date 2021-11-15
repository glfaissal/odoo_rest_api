from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel
from odoo.addons.datamodel.fields import NestedModel


class ArticleInfo(Datamodel):
    _name = "article.info"
    _inherit = "article.short.info"

    description = fields.String(required=False, allow_none=True)
    article_type = fields.String(required=True, allow_none=False)
    categ_id = fields.Integer(required=True, allow_none=False)
