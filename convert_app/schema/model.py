import datetime
from decimal import Decimal


class RequestModel:
    def __init__(self, amount: Decimal = None, src_currency: str = None, dest_currency: str = None,
                 reference_date: datetime.date = None) -> None:
        self.amount = amount
        self.src_currency = src_currency
        self.dest_currency = dest_currency
        self.reference_date = reference_date

    def convert(self) -> dict:
        return {"amount": 0.3, "currency": "EUR"}
