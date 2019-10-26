import datetime
from argparse import Namespace

from flask import current_app, Response
from flask.views import MethodView
from werkzeug.exceptions import InternalServerError

from convert_app.api.v1.views_template import TemplateView
from convert_app.db.mongo_db.repo import populate_db_from_object
from convert_app.schema.schema import UpdateDbResponseSchema


class UpdateDbView(MethodView):

    def get(self):
        try:
            config_object = Namespace(**current_app.config)
            total_inserted = populate_db_from_object(config_object)
            result = {"total_inserted": total_inserted}
            status = 200
        except Exception as e:
            result = {"error_message": f"An exception occurred while handling the request: {e}"}
            status = InternalServerError.code
        execution_date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
        result.update({"date": execution_date})
        response_schema_result = UpdateDbResponseSchema().dump(result)
        return Response(response_schema_result, status=status, mimetype='application/json')


class UpdateDbTemplateView(TemplateView):
    template_name = "api/v1/update_db.html"
