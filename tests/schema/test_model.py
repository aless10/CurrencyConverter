from decimal import Decimal

import pytest

from convert_app.schema.model import RequestModel


def test_convert_method():
    request_model = RequestModel(amount=Decimal(10.0), src_currency="USD", dest_currency="EUR",
                                 reference_date="2019-10-28")
    result = request_model.convert()
    assert isinstance(result, dict)
    assert pytest.approx(result["amount"], rel=Decimal(0.1)) == Decimal(3.0)
    assert result["currency"] == "EUR"
