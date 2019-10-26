from flask import Blueprint

from convert_app.api.v1.convert_task_view import ConvertView, ConvertTemplateView
from convert_app.api.v1.status import Status, TemplateStatus
from convert_app.api.v1.update_db_view import UpdateDbView, UpdateDbTemplateView

v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

views_v1 = Blueprint('views_v1', __name__, url_prefix='/views/v1')


v1.add_url_rule('/status', view_func=Status.as_view('get_status'))
v1.add_url_rule('/convert', view_func=ConvertView.as_view('convert'))
v1.add_url_rule('/update-db', view_func=UpdateDbView.as_view('update_db'))


views_v1.add_url_rule('/status', view_func=TemplateStatus.as_view('get_status'))
views_v1.add_url_rule('/convert', view_func=ConvertTemplateView.as_view('convert'))
views_v1.add_url_rule('/update-db', view_func=UpdateDbTemplateView.as_view('update_db'))
