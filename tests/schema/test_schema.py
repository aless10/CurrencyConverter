from decimal import Decimal

import pytest
from marshmallow import ValidationError

from convert_app.schema.schema import RequestSchema


def test_request_schema_valid():
    request_body = {"amount": Decimal(12.95),
                    "src_currency": "EUR",
                    "dest_currency": "USD",
                    "reference_date": "2019-10-30"}
    request_model = RequestSchema().load(request_body)
    assert request_model.amount == Decimal(12.95)
    assert request_model.src_currency == "EUR"
    assert request_model.dest_currency == "USD"
    assert request_model.reference_date == "2019-10-30"


def test_request_schema_invalid_currency():
    request_body = {"amount": Decimal(12.95),
                    "src_currency": "TOOLONGCURRENCY",
                    "dest_currency": "EUR",
                    "reference_date": "2019-10-30"}
    with pytest.raises(ValidationError):
        RequestSchema().load(request_body)


def test_request_schema_invalid_date():
    request_body = {"amount": Decimal(12.95),
                    "src_currency": "EUR",
                    "dest_currency": "USD",
                    "reference_date": "20191030"}
    with pytest.raises(ValidationError):
        RequestSchema().load(request_body)


def test_request_schema_invalid_amount():
    request_body = {"amount": "not a amount value",
                    "src_currency": "EUR",
                    "dest_currency": "USD",
                    "reference_date": "2019-10-30"}
    with pytest.raises(ValidationError):
        RequestSchema().load(request_body)
