# Copyright 2020 Camptocamp SA (http://www.camptocamp.com)
# @author Simone Orsi <simahawk@gmail.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import contextlib

from odoo.addons.base_rest import restapi
from odoo.addons.base_rest.tests.common import SavepointRestServiceRegistryCase
from odoo.addons.component.core import Component
from odoo.addons.website.tools import MockRequest


class TestDBLoggingBase(SavepointRestServiceRegistryCase):
    """Test DB logging for REST calls."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.base_url = cls.env["ir.config_parameter"].get_param("web.base.url")
        cls.service = cls._get_service(cls)
        cls.log_model = cls.env["rest.log"].sudo()

    @staticmethod
    def _get_service(class_or_instance):
        # pylint: disable=R7980
        class LoggedService(Component):
            _inherit = "base.rest.service"
            _name = "test.log.service"
            _usage = "logmycalls"
            _collection = class_or_instance._collection_name
            _description = "Test log my calls"
            _log_calls_in_db = True

            @restapi.method(
                [(["/<int:id>/get", "/<int:id>"], "GET")],
                output_param=restapi.CerberusValidator("_get_out_schema"),
                auth="public",
            )
            def get(self, _id):
                """Get some information"""
                return {"name": "Mr Logger"}

            def _get_out_schema(self):
                return {"name": {"type": "string", "required": True}}

        class_or_instance.comp_registry.load_components("rest_log")
        # class_or_instance._build_services(class_or_instance, LoggedService)
        # TODO: WTH _build_services does not load the component?
        LoggedService._build_component(class_or_instance.comp_registry)
        return class_or_instance._get_service_component(class_or_instance, "logmycalls")

    @contextlib.contextmanager
    def _get_mocked_request(self, httprequest=None, extra_headers=None):
        with MockRequest(self.env) as mocked_request:
            mocked_request.httprequest = httprequest or mocked_request.httprequest
            headers = {"Cookie": "IaMaCookie!", "Api-Key": "I_MUST_STAY_SECRET"}
            headers.update(extra_headers or {})
            mocked_request.httprequest.headers = headers
            yield mocked_request
