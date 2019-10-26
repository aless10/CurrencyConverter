import logging

from flask import make_response, jsonify
from flask.views import MethodView

from convert_app.api.v1.views_template import TemplateView

log = logging.getLogger(__name__)


class Status(MethodView):

    def get(self):
        """
        Returns the status of the application
        ---
        responses:
          200:
            description: Returns a json with alive as key
        """
        log.info("Calling the endpoint")
        return make_response(jsonify({"alive": True}))


class TemplateStatus(TemplateView):
    template_name = "api/v1/status.html"
