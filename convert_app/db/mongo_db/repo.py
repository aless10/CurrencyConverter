import logging

from convert_app.db.mongo_db.session import context_db
from convert_app.xml_data.importer import XMLElement

log = logging.getLogger(__name__)


def populate_db_from_object(config_obj):
    data = XMLElement.from_url(config_obj.SOURCE_URL)
    collection_name = "currency"
    with context_db(config_obj.DATABASE_CONNECTION_URI) as db:
        coll = getattr(db, str(collection_name))
        if coll.count() == 0:
            log.info("initialize collection %s", collection_name)
            coll.insert_many({k: v for k, v in data.items()})
        else:
            log.info("collection %s already populated. Skipping", collection_name)
