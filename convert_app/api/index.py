from flask import url_for, Blueprint, redirect
from flask.views import MethodView


class IndexView(MethodView):

    def get(self):
        return redirect(url_for("swagger_ui.show"))


index = Blueprint('index', __name__)
index.add_url_rule("/", view_func=IndexView.as_view('index'))
