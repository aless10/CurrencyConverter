import logging

from flask import request, Response
from marshmallow import ValidationError
from werkzeug.exceptions import BadRequest, InternalServerError, NotFound

from convert_app.db.exceptions import RateNotFound
from convert_app.schema.schema import RequestSchema, ResponseSchema

log = logging.getLogger(__name__)


class TaskExecutor:

    def __init__(self):
        self._result = None
        self._status_code = None

    def execute(self):
        request_body = request.args
        log.info("Running converter task with args %s", request_body)
        try:
            request_model = RequestSchema().load(request_body)
        except ValidationError as e:
            log.error('Failed Schema Validation: %s', e)
            self._status_code = BadRequest.code
        except Exception as e:
            log.error('Error while validating schema: %s', e)
            self._status_code = InternalServerError.code
        else:
            try:
                self._result = request_model.convert()
                log.info("Task result: %s", self._result)
                self._status_code = 200
            except RateNotFound:
                log.info("Rate value not found")
                self._status_code = NotFound.code
            except Exception:
                log.exception("Exception occurred in task")
                self._status_code = InternalServerError.code

    def make_response(self):
        response_schema_result = ResponseSchema().dump(self._result)
        return Response(response_schema_result, status=self._status_code, mimetype='application/json')
