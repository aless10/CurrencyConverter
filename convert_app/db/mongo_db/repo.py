import logging
from decimal import Decimal

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
        if coll.count() == 0:
            log.info("initialize collection %s", COLLECTION_NAME)
            coll.insert_many(data.items())
            i = coll.count()
        else:
            log.info("Updating collection %s with new data", COLLECTION_NAME)
            for element in data.items():
                if not coll.find({"time": element['time']}).count():
                    log.info("Insert element %s into collection", element)
                    coll.insert(element)
                    i += 1
                else:
                    log.info("No new data found")
                    break
        return i


def get_rate_by_date_currency(ref_date: str, currency: str) -> Decimal:
    if currency == "EUR":
        return Decimal(1)
    else:
        return Decimal(3)
