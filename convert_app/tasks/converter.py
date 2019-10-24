import logging
from decimal import Decimal
from typing import Optional

from convert_app.db.mongo_db.repo import get_rate_by_date_currency

log = logging.getLogger(__name__)


def get_rate(reference_date: str, currency: str) -> Optional[Decimal]:
    return get_rate_by_date_currency(reference_date, currency)


def convert_to_euro(amount: Decimal, rate: Decimal) -> Decimal:
    return amount * rate


def convert_from_euro(amount: Decimal, rate: Decimal) -> Decimal:
    try:
        return amount / rate
    except ZeroDivisionError:
        log.error("Rate should not be equal to 0")
        raise


def convert(reference_date: str, src_cur: str, dst_cur: str, amount: Decimal) -> Decimal:
    log.info("Converting %s from %s to %s at date %s", amount, src_cur, dst_cur, reference_date)
    src_rate = get_rate(reference_date, src_cur)
    dst_rate = get_rate(reference_date, dst_cur)
    euro_amount = convert_to_euro(amount, src_rate)
    dst_amount = convert_from_euro(euro_amount, dst_rate)
    log.info("Result amount is %s %s", dst_amount, dst_cur)
    return dst_amount
