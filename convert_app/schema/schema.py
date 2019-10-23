import datetime

import simplejson as json

from marshmallow import Schema, fields, post_load, post_dump, validates, ValidationError

from convert_app.schema.model import RequestModel

TWOPLACES = 2


def validate_currency(value):
    if len(value) != 3:
        raise ValidationError("Currency must be in ISO format.")


class RequestSchema(Schema):
    amount = fields.Decimal(required=True, description="the amount to convert(e.g. 12.35)")
    src_currency = fields.Str(required=True, validate=validate_currency,
                              description="ISO currency code for the source currency to convert (e.g. EUR, USD, GBP)")
    dest_currency = fields.Str(required=True, validate=validate_currency,
                               description="ISO currency code for the destination currency to convert "
                                           "(e.g. EUR, USD, GBP)")
    reference_date = fields.Str(required=True,
                                description="reference date for the exchange rate, in YYYY-MM-DD format")

    @validates("amount")
    def validate_amount(self, value):
        if value < 0:
            raise ValidationError("Amount to be converted must be >= 0.")

    @validates("reference_date")
    def validate_date_format(self, value):
        try:
            datetime.datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise ValidationError("Reference date must be in format YYYY-MM-DD.")

    @post_load
    def make_request(self, data, **kwargs):  # pylint: disable=unused-argument
        return RequestModel(**data)


class ResponseSchema(Schema):
    amount = fields.Decimal(description="Converted amount", default=None, places=TWOPLACES)
    currency = fields.Str(default=None)

    @post_dump
    def to_json(self, data, **kwargs):  # pylint: disable=unused-argument
        return json.dumps(data)
