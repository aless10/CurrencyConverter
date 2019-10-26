from flask import render_template
from flask.views import MethodView


class TemplateView(MethodView):

    template_name = None

    def get(self, *args, **kwargs):
        return render_template(template_name_or_list=self.template_name)
