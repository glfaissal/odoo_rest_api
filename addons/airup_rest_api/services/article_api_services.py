from odoo.addons.base_rest import restapi
from odoo.addons.base_rest_datamodel.restapi import Datamodel
from odoo.addons.component.core import Component

from pprint import pprint as pp


class ArticleApiService(Component):
    _inherit = "base.rest.service"
    _name = "article.new_api.service"
    _usage = "article"
    _collection = "base.rest.demo.new_api.services"
    _description = """
        Partner New API Services
        Services developed with the new api provided by base_rest
    """

    @restapi.method(
        [(["/<int:id>/get", "/<int:id>"], "GET")],
        output_param=Datamodel("article.info"),
        auth="public",
    )
    def get(self, _id):
        """
        Get Article's information
        """
        article = self._get(_id)
        ArticleInfo = self.env.datamodels["article.info"]
        article_info = ArticleInfo(partial=True)
        article_info.id = article.id
        article_info.name = article.name
        article_info.description = article.description_sale
 
        return article_info

    @restapi.method(
        [(["/", "/search"], "GET")],
        input_param=Datamodel("article.search.param"),
        output_param=Datamodel("article.short.info", is_list=True),
        auth="public",
    )
    def search(self, article_search_param):
        """
        Search for article
        :param partner_search_param: An instance of partner.search.param
        :return: List of article.short.info
        """
        domain = []
        if article_search_param.name:
            domain.append(("name", "like", article_search_param.name))
        if article_search_param.id:
            domain.append(("id", "=", article_search_param.id))
        res = []
        ArticleShortInfo = self.env.datamodels["article.short.info"]
        for a in self.env["product.template"].search(domain):
            res.append(ArticleShortInfo(id=a.id, name=a.name))
        return res

    # The following method are 'private' and should be never never NEVER call
    # from the controller.

    def _get(self, _id):
        return self.env["product.template"].browse(_id)


    def _to_json(self, article):
        return {
            "id": article.id,
            "name": article.name,
            "description": article.description
        }

    # pylint:disable=method-required-super
    def create(self, **params):
        """
        Create a new article
        """
        article = self.env["product.template"].create(params)
        return self._to_json(article)

    # Validator
    def _validator_return_get(self):
        res = self._validator_create()
        res.update({"id": {"type": "integer", "required": True, "empty": False}})
        return res

    def _validator_create(self):
        res = {
            "name": {"type": "string", "required": True, "empty": False},
            "description": {"type": "string", "required": True, "empty": False}
        }
        return res

    def _validator_update(self):
        res = self._validator_create()
        for key in res:
            if "required" in res[key]:
                del res[key]["required"]
        return res

    def _validator_return_update(self):
        return self._validator_return_get()

    def update(self, _id, **params):
        """
        Update partner informations
        """
        article = self._get(_id)
        article.write(params)
        return self._to_json(article)

    def delete(self, _id):
        """
        Delete method description ...
        """
        article = self._get(_id)
        article.unlink()

        return {"response": "DELETE called with id %s " % _id}