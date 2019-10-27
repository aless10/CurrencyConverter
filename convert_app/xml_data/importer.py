from xml.etree import ElementTree
import requests
from requests import RequestException

from convert_app.db.mongo_db.model import Document
from convert_app.utils.decorators import retry


class XMLElement:

    def __init__(self, data):
        self.data = data

    @classmethod
    def from_url(cls, url: str) -> 'XMLElement':
        data = get_data_from_url(url)
        xml_obj = get_xml_from_string(data)[2]
        data = serialize_from_xml_element(xml_obj)
        return cls(data)

    def items(self):
        for element in self.data:
            yield element


@retry(exceptions=(RequestException, ConnectionError, Exception), tries=4, delay=3, backoff=2)
def get_data_from_url(url: str) -> str:
    r = requests.get(url)
    return r.content


def get_xml_from_string(xml_str: str) -> ElementTree:
    return ElementTree.fromstring(xml_str)


def serialize_from_xml_element(xml_element: ElementTree) -> list:
    r = []
    for item in xml_element:
        for sub_item in item:
            document = Document(time=item.get("time"), **dict(sub_item.items()))
            r.append(document.to_dict())
    return r
