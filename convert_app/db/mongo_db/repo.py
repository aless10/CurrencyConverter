import logging
from decimal import Decimal
from typing import Optional

from flask import current_app

from convert_app.db.exceptions import RateNotFound
from convert_app.db.mongo_db.session import context_db
from convert_app.xml_data.importer import XMLElement

log = logging.getLogger(__name__)

DATABASE_CONNECTION_URI = "DATABASE_CONNECTION_URI"
COLLECTION_NAME = "currency"


def populate_db_from_object(config_obj):
    data = XMLElement.from_url(config_obj.SOURCE_URL)
    with context_db(config_obj.DATABASE_CONNECTION_URI) as db:
        coll = getattr(db, COLLECTION_NAME)
        i = 0
        if coll.count_documents({}) == 0:
            log.info("initialize collection %s", COLLECTION_NAME)
            coll.insert_many(data.items())
            i = coll.count_documents({})
        else:
            log.info("Updating collection %s with new data", COLLECTION_NAME)
            for element in data.items():
                if coll.find_one({"time": element['time']}) is None:
                    log.info("Insert element %s into collection", element)
                    coll.insert(element)
                    i += 1
                else:
                    log.info("No new data found")
                    break
        return i


def get_rate_by_date_currency(ref_date: str, currency: str) -> Optional[Decimal]:
    if currency == "EUR":
        return Decimal(1)
    else:
        with context_db(current_app.config[DATABASE_CONNECTION_URI]) as db:
            rate = db.get_collection(COLLECTION_NAME).find_one({"currency": currency, "time": ref_date},
                                                               {"rate": 1, "_id": 0})
            if rate is not None:
                return Decimal(rate.get("rate"))
            else:
                raise RateNotFound(f"Rate for currency {currency} and reference_date {ref_date} not found.")
