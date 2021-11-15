from odoo.addons.base_rest import restapi
from odoo.addons.base_rest_datamodel.restapi import Datamodel
from odoo.addons.component.core import Component

from pprint import pprint as pp

class WarehouseApiService(Component):
    _inherit = "base.rest.service"
    _name = "warehouse.new_api.service"
    _usage = "warehouse"
    _collection = "base.rest.demo.new_api.services"
    _description = """
        warehouse New API Services
        Services developed with the new api provided by base_rest
    """

    @restapi.method(
        [(["/"], "GET")],
        output_param=Datamodel("warehouse.shorter.info", is_list=True),
        auth="public",
    )
    def get(self):
        """
        Get warehouse's information
        """
        WarehouseShortInfo = self.env.datamodels["warehouse.shorter.info"]
        res = []
        for product in self.env["product.product"].search([]):
            #product_quantity = sum([ quant.quantity for quant in self.env["stock.quant"].search([("product_id","=",product.id)])])
            res.append(WarehouseShortInfo(id=product.id, name=product.name, amount=product.qty_available))
        #res.append(WarehouseShortInfo(id=1, name=p.name, amount=7))
        return res

    @restapi.method(
        [(["/", "/search"], "GET")],
        input_param=Datamodel("warehouse.search.param"),
        output_param=Datamodel("warehouse.article.shelfs", is_list=True),
        auth="public",
    )
    def search(self, warehouse_search_param):
        """
        Search for warehouse
        :param partner_search_param: An instance of partner.search.param
        :return: List of warehouse.article.shelfs
        """
        domain_id = []
        domain_row_bay = []
        products = []

        if warehouse_search_param.row:
            domain_row_bay.append(("row", "=", warehouse_search_param.row))
        if warehouse_search_param.bay:
            domain_row_bay.append(("bay", "=", warehouse_search_param.bay))
        if warehouse_search_param.id:
            products.append(warehouse_search_param.id)
            #domain_id.append(("id", "=", warehouse_search_param.id))

        if warehouse_search_param:
            locations = self.env["stock.location"].search(domain_row_bay)
            for location in locations:
                quants = self.env["stock.quant"].search([('location_id','=',location.id)])
                for quant in quants:
                    if quant.product_id.id not in products:
                        products.append(quant.product_id.id)

        res = []
        rows= []
        WarehouseArticleShelfs = self.env.datamodels["warehouse.article.shelfs"]
        ShelfDetailInfo = self.env.datamodels["shelf.detail.warehouse"]
        for w in self.env["product.product"].browse(products):
            product_locations = []  

            # get all locations of the product
            unique_locations = []
            shelfsDetailInfo = []
            stock_quants = self.env["stock.quant"].search([("product_id","=",w.id)])
            for s in stock_quants:
                if s.location_id.name not in unique_locations and s.location_id.usage not in ['view','inventory']:
                    unique_locations.append(s.location_id.id)
                    available_qty = w.with_context({'location' : s.location_id.id}).qty_available
                    #rows.append(s.location_id.row)
                    shelfsDetailInfo.append(ShelfDetailInfo(amount=available_qty, bay=s.location_id.bay if s.location_id.bay else "bay to be assigned", row=s.location_id.row if s.location_id.row else "row to be assigned" ))


            res.append(WarehouseArticleShelfs(id=w.id, name=w.name, shelfs=shelfsDetailInfo, debug = str(rows)))
        return res


    # Validator
    def _validator_return_get(self):
        res = {
            "id": {"type": "integer", "required": False, "empty": True},
            "name": {"type": "string", "required": False, "empty": True},
            "amount": {"type": "integer", "required": False, "empty": True}
            }

        return res

    def _validator_create(self):
        res = {
            "id": {"type": "integer", "required": False, "empty": True},
            "name": {"type": "string", "required": False, "empty": True},
            "amount": {"type": "integer", "required": False, "empty": True}
            }

        return res