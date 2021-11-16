from odoo.addons.base_rest import restapi
from odoo.addons.base_rest_datamodel.restapi import Datamodel
from odoo.addons.component.core import Component

from pprint import pprint as pp

class ShelfApiService(Component):
    _inherit = "base.rest.service"
    _name = "shelf.new_api.service"
    _usage = "shelfs"
    _collection = "base.rest.api.services"
    _description = """
        Shelfs New API Services
        Services developed with the new api provided by base_rest
    """

    @restapi.method(
        [(["/<string:row>"], "GET")],
        output_param=Datamodel("shelf.short.info", is_list=True),
        auth="public",
    )
    def get_by_row(self, _row):
        """
        Get Shelf's information
        """

        domain = []
        domain.append(("is_shelf", "=", True))
        if _row:
            domain.append(("row", "like", _row))
        res = []
        ShelfShortInfo = self.env.datamodels["shelf.short.info"]
        for s in self.env["stock.location"].search(domain):
            res.append(ShelfShortInfo(id=s.id, name=s.name, bay=s.bay))
        return res

    @restapi.method(
        [(["/<string:row>/<string:bay>"], "GET")],
        output_param=Datamodel("shelf.short.info", is_list=True),
        auth="public",
    )
    def get_by_row_and_bay(self, _row, _bay):
        """
        Get Shelf's information
        """
        domain = []
        domain.append(("is_shelf", "=", True))
        if _row:
            domain.append(("row", "=", _row))
        if _bay:
            domain.append(("bay", "=", _bay))
        res = []
        ShelfShortInfo = self.env.datamodels["shelf.info"]
        for s in self.env["stock.location"].search(domain):
            res.append(ShelfShortInfo(id=s.id, name=s.name, row=s.row, bay=s.bay, width=s.width, height=s.height, depth=s.depth))
        return res


    @restapi.method(
        [(["/", "/search"], "GET")],
        input_param=Datamodel("shelf.search.param"),
        output_param=Datamodel("shelf.short.info", is_list=True),
        auth="public",
    )
    def search(self, shelf_search_param):
        """
        Search for shelf
        :param shelf_search_param: An instance of shelf.search.param
        :return: List of shelf.short.info
        """
        domain = []
        domain.append(("is_shelf", "=", True))
        if shelf_search_param.name:
            domain.append(("name", "like", shelf_search_param.name))
        if shelf_search_param.id:
            domain.append(("id", "=", shelf_search_param.id))
        res = []
        ShelfShortInfo = self.env.datamodels["shelf.short.info"]
        for s in self.env["stock.location"].search(domain):
            res.append(ShelfShortInfo(id=s.id, name=s.name, row=s.row, bay=s.bay))
        return res

    # The following method are 'private' and should be never never NEVER call
    # from the controller.

    def _get(self, _id):
        return self.env["stock.location"].browse(shelf.id)

    def _get_by_row_and_bay(self, _row, _bay):
        domain = []
        domain.append(("is_shelf", "=", True))
        domain.append(("row", "=", _row))
        domain.append(("bay", "=", _bay))
        shelf = self.env["stock.location"].search(domain)
            
        return self.env["stock.location"].browse(shelf[0].id)

    def _to_json(self, shelf):
        return {
            "id": shelf.id,
            "name": shelf.name
            #"description": shelf.description
        }

    # pylint:disable=method-required-super
    def create(self, **params):
        """
        Create a new article
        """
        # todo
        # Get row Param
        # search for location where parent = bay param and grand parent is row param
        shelf = self.env["stock.location"].create(params)
        return self._to_json(shelf)

    # Validator
    def _validator_return_get(self):
        res = self._validator_create()
        res.update({"id": {"type": "integer", "required": True, "empty": False}})
        return res

    def _validator_create(self):
        res = {
            "name": {"type": "string", "required": True, "empty": False},
            "is_shelf": {"type": "boolean", "required": False, "empty": True},
            "row": {"type": "string", "required": False, "empty": True},
            "bay": {"type": "string", "required": False, "empty": True},
            "width": {"type": "float", "required": False, "empty": True},
            "height": {"type": "float", "required": False, "empty": True},
            "depth": {"type": "float", "required": False, "empty": True}
        }
        return res

    def _validator_patch(self):
        res = {
            "name": {"type": "string", "required": True, "empty": False},
            "is_shelf": {"type": "boolean", "required": False, "empty": True},
            "row": {"type": "string", "required": False, "empty": True},
            "bay": {"type": "string", "required": False, "empty": True},
            "width": {"type": "float", "required": False, "empty": True},
            "height": {"type": "float", "required": False, "empty": True},
            "depth": {"type": "float", "required": False, "empty": True}
        }
        return res

    # def _validator_update(self):
    #     res = self._validator_create()
    #     for key in res:
    #         if "required" in res[key]:
    #             del res[key]["required"]
    #     return res

    def _validator_return_update(self):
        return self._validator_return_get()

    def update(self, _row, message):
        """
        Update shelf informations
        """
        params = {}
        shelf = self._get_by_row_and_bay(params.get('row'), params.get('bay'))
        shelf.write(params)
        return self._to_json(shelf)

    @restapi.method(
        [(["/<string:row>/<string:bay>"], "PATCH")],
        input_param=restapi.Datamodel("shelf.shorter.info"),
        #output_param=Datamodel("shelf.info"),
        auth="public",
    )
    def update_shelf(self, row, bay, params):
        """
        Get Shelf's information
        """
        #self.env["stock.location"].search([("row","=",row),("bay","=",bay)])[0].write(params)
        self.env["stock.location"].search([("row","=",row),("bay","=",bay)])[0].write({'depth': params.depth})
        #shelf = self._get_by_row_and_bay(row, bay)
        #shelf.write(params)
        return {"response": "Update called"}
        #return self._to_json(shelf)

    @restapi.method(
        [(["/<string:row>/<string:bay>"], "DELETE")],
        auth="public",
    )
    def delete_shelf(self, row, bay):
        """
        Get Shelf's information
        """
        #shelf = self._get_by_row_and_bay(row, bay)
        self.env["stock.location"].search([("row","=",row),("bay","=",bay)]).unlink()
        #shelf.unlink()
        return {"response": "DELETE called"}

    def delete(self, _id):
        """
        Delete method description ...
        """
        shelf = self._get(_id)
        shelf.unlink()

        return {"response": "DELETE called with id %s " % _id}
