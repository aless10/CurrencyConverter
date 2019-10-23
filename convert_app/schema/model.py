from decimal import Decimal

from convert_app.tasks.converter import convert


class RequestModel:
    def __init__(self, amount: Decimal = None, src_currency: str = None, dest_currency: str = None,
                 reference_date: str = None) -> None:
        self.amount = amount
        self.src_currency = src_currency
        self.dest_currency = dest_currency
        self.reference_date = reference_date

    def convert(self) -> dict:
        dst_amount = convert(self.reference_date,
                             self.src_currency,
                             self.dest_currency,
                             self.amount)
        return {"amount": dst_amount, "currency": self.dest_currency}
