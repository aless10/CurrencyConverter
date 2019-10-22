import datetime
from decimal import Decimal

from convert_app.schema.model import RequestModel


def test_convert_method():
    request_model = RequestModel(amount=Decimal(10.0), src_currency="USD", dest_currency="EUR",
                                 reference_date=datetime.date(2019, 10, 28))
    assert request_model.convert() == {"amount": 0.3, "currency": "EUR"}
