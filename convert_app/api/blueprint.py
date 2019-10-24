from flask import Blueprint

from convert_app.api.v1.convert_task_view import ConvertView
from convert_app.api.v1.status import Status
from convert_app.api.v1.update_db_view import UpdateDbView

v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

v1.add_url_rule('/status', view_func=Status.as_view('get_status'))
v1.add_url_rule('/convert', view_func=ConvertView.as_view('convert'))
v1.add_url_rule('/update-db', view_func=UpdateDbView.as_view('update_db'))
