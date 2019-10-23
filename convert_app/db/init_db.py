import logging

from convert_app.db.mongo_db.repo import populate_db_from_object

log = logging.getLogger(__name__)


def init_db(config_obj):
    log.info("Init db from url %s", config_obj.SOURCE_URL)
    populate_db_from_object(config_obj)
