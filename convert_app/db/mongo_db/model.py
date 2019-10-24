class Document:
    def __init__(self, time: str, currency: str, rate: str) -> None:
        self.time = time
        self.currency = currency
        self.rate = rate

    def to_dict(self) -> dict:
        return {"time": self.time,
                "currency": self.currency,
                "rate": self.rate}
