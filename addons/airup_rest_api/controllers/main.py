# Copyright 2018 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.base_rest.controllers import main


class BaseRestDemoPublicApiController(main.RestController):
    _root_path = "/api/public/"
    _collection_name = "base.rest.airup.public.services"
    _default_auth = "public"


class BaseRestDemoNewApiController(main.RestController):
    _root_path = "/api/"
    _collection_name = "base.rest.api.services"
    _default_auth = "public"
