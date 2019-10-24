from decimal import Decimal

import pytest

from convert_app.tasks.converter import get_rate, convert_to_euro, convert_from_euro


def test_get_rate_euro():
    assert get_rate("2019-10-24", "EUR") == Decimal(1)


def test_get_rate():
    assert get_rate("2019-10-24", "USD") == Decimal(3)


def test_convert_to_euro():
    test_amount = Decimal(12.95)
    test_rate = Decimal(1.2)
    assert convert_to_euro(test_amount, test_rate) == Decimal('15.53999999999999857225319033')


def test_convert_from_euro():
    test_amount = Decimal(12.95)
    test_rate = Decimal(1.2)
    assert convert_from_euro(test_amount, test_rate) == Decimal('10.79166666666666647391961378')


def test_convert_from_euro_zero_rate():
    with pytest.raises(ZeroDivisionError):
        convert_from_euro(Decimal(0.1), Decimal(0))
