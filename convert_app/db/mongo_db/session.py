import logging
from contextlib import contextmanager

import pymongo

log = logging.getLogger(__name__)


def create_db(connection_string: str) -> pymongo.collection:
    client = pymongo.MongoClient(connection_string)
    return client.convert_db


@contextmanager
def context_db(connection_string: str) -> None:
    log.debug("Creating mongo db context")
    db = create_db(connection_string)
    log.debug("Session created")
    try:
        yield db
    except Exception as e:
        log.error("exception occurred while using session: %s", e)
        raise e
    finally:
        db.client.close()
        log.debug("Session Closed")
