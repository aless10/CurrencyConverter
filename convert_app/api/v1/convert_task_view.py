from flask.views import MethodView

from convert_app.api.v1.views_template import TemplateView
from convert_app.cache.cache_utils import cache
from convert_app.tasks.task_executor import TaskExecutor


class ConvertView(MethodView):

    @cache
    def get(self, *args, **kwargs):
        executor = TaskExecutor()
        executor.execute()
        return executor.make_response()


class ConvertTemplateView(TemplateView):
    template_name = "api/v1/convert.html"
