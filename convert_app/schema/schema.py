import simplejson as json

from marshmallow import Schema, fields, post_load, post_dump, validates, ValidationError

from convert_app.schema.model import RequestModel


class RequestSchema(Schema):
    amount = fields.Decimal(required=True, description="the amount to convert(e.g. 12.35)")
    src_currency = fields.Str(required=True,
                              description="ISO currency code for the source currency to convert (e.g. EUR, USD, GBP)")
    dest_currency = fields.Str(required=True,
                               description="ISO currency code for the source currency to convert (e.g. EUR, USD, GBP)")
    reference_date = fields.Date(required=True,
                                 description="reference date for the exchange rate, in YYYY-MM-DD format")

    @validates("dest_currency")
    @validates("src_currency")
    def validate_currency(self, value):
        if len(value) != 3:
            raise ValidationError("Currency must be in ISO format.")

    @post_load
    def make_request(self, data, **kwargs):  # pylint: disable=unused-argument
        return RequestModel(**data)


class ResponseSchema(Schema):
    amount = fields.Decimal(description="Converted amount", default=None)
    currency = fields.Str(default=None)

    @post_dump
    def to_json(self, data, **kwargs):  # pylint: disable=unused-argument
        return json.dumps(data)
