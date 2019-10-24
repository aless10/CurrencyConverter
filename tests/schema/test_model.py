from decimal import Decimal
from unittest import mock

import pytest
from convert_app.schema.model import RequestModel


@mock.patch("convert_app.tasks.converter.get_rate", side_effect=[Decimal(1.11), Decimal(1)])
def test_convert_method(app):
    request_model = RequestModel(amount=Decimal(10.0), src_currency="USD", dest_currency="EUR",
                                 reference_date="2019-10-28")
    result = request_model.convert()
    assert isinstance(result, dict)
    assert pytest.approx(result["amount"], rel=Decimal(0.1)) == Decimal(11.1)
    assert result["currency"] == "EUR"


def test_convert_method_nothing_to_convert(app):
    request_model = RequestModel(amount=Decimal(10.0), src_currency="EUR", dest_currency="EUR",
                                 reference_date="2019-10-28")
    result = request_model.convert()
    assert result["amount"] == Decimal(10.0)
