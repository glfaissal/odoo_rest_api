# Copyright 2018 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.base_rest.controllers import main


class BaseRestAirupPublicApiController(main.RestController):
    _root_path = "/airup/public/"
    _collection_name = "base.rest.airup.public.services"
    _default_auth = "public"


class BaseRestAirupApiController(main.RestController):
    _root_path = "/airup/api/"
    _collection_name = "base.rest.airup.api.services"
    _default_auth = "public"
