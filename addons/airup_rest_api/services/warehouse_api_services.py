from odoo.addons.base_rest import restapi
from odoo.addons.base_rest_datamodel.restapi import Datamodel
from odoo.addons.component.core import Component

from pprint import pprint as pp

class WarehouseApiService(Component):
    _inherit = "base.rest.service"
    _name = "warehouse.new_api.service"
    _usage = "warehouse"
    _collection = "base.rest.api.services"
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
            #domain_row_bay.append(("id", "=", warehouse_search_param.id))

        if domain_row_bay:
            locations = self.env["stock.location"].search(domain_row_bay)
            for location in locations:
                quants = self.env["stock.quant"].search([('location_id','=',location.id)])
                for quant in quants:
                    if quant.product_id.id not in products and not warehouse_search_param.id:
                        products.append(quant.product_id.id)

        res = []
        rows= []
        WarehouseArticleShelfs = self.env.datamodels["warehouse.article.shelfs"]
        ShelfDetailInfo = self.env.datamodels["shelf.detail.warehouse"]
        for w in self.env["product.product"].browse(products):
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


    @restapi.method(
        [(["/"], "POST")],
        input_param=restapi.Datamodel("warehouse.load.number"),
        output_param=Datamodel("warehouse.debug"),
        auth="public",
    )
    def post_transfert(self, params):
        """
        transfert qte of product in a Shelf
        """
        picking_type_id = self.env["stock.picking.type"].search(
            [("name","=","Internal Transfers")])[0].id
        location_id = self.env["stock.location"].search(
            [("name","=","Vendors")])[0].id
        location_dest_id = self.env["stock.location"].search(
            [("is_shelf","=",True),("row","=",params.row),("bay","=",params.bay)])[0].id

        product_uom = self.env["uom.uom"].search(
            [("name","=","Units")], limit=1).id

        random_name = ''.join((random.choice(string.ascii_lowercase) for x in range(10))) 

        move_line = {
            "name": random_name,
            "product_uom":product_uom,
            "product_id":params.id,
            "product_uom_qty":params.amount
        }

        transfert_object =self.env["stock.picking"].create(
            {
                #"name": random_name,
                "picking_type_id":picking_type_id,
                "location_id":location_id,
                "location_dest_id":location_dest_id,
                "move_ids_without_package":[(0, 0, move_line)]
            })
        transfert_object.action_confirm()
        transfert_object.button_validate()

        Debugger = self.env.datamodels["warehouse.debug"]
        return Debugger(console="operation type " + str(picking_type_id) + "location_id" +  str(location_id)+ "location_dest_id" + str(location_dest_id) + "  move line " + str(move_line))


    @restapi.method(
        [(["/"], "PUT")],
        input_param=restapi.Datamodel("warehouse.load.number"),
        output_param=Datamodel("warehouse.debug"),
        auth="public",
    )
    def put_pick_article(self, params):
        """
        transfert qte of product in a Shelf
        """
        picking_type_id = self.env["stock.picking.type"].search(
            [("name","=","Internal Transfers")], limit=1).id
        location_dest_id = self.env["stock.location"].search(
            [("name","=","Customers")], limit=1).id
        location_id = self.env["stock.location"].search(
            [("row","=",params.row),("bay","=",params.bay)], limit=1).id

        product_uom = self.env["uom.uom"].search(
            [("name","=","Units")], limit=1).id

        random_name = ''.join((random.choice(string.ascii_lowercase) for x in range(10))) 

        move_line = {
            "name": random_name,
            "product_uom":product_uom,
            "product_id":params.id,
            "product_uom_qty": 1
        }

        transfert_object =self.env["stock.picking"].create(
            {
                #"name": random_name,
                "picking_type_id":picking_type_id,
                "location_id":location_id,
                "location_dest_id":location_dest_id,
                "move_ids_without_package":[(0, 0, move_line)]
            })
        transfert_object.action_confirm()
        #transfert_object.button_validate()

        Debugger = self.env.datamodels["warehouse.debug"]
        return Debugger(console="operation type " + str(picking_type_id) + "location_id" +  str(location_id)+ "location_dest_id" + str(location_dest_id) + "  move line " + str(move_line))




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
