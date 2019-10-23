from collections import defaultdict

from lxml import etree
from lxml.etree import Element
import requests


class XMLElement:

    def __init__(self, data):
        self.data = data

    @classmethod
    def from_url(cls, url: str) -> 'XMLElement':
        data = get_data_from_url(url)
        xml_obj = get_xml_from_string(data)[2]
        data = get_dict_from_xml_element(xml_obj)
        return cls(data)

    def items(self):
        return self.data.items()


def get_data_from_url(url: str) -> str:
    r = requests.get(url)
    return r.content


def get_xml_from_string(xml_str: str) -> Element:
    return etree.fromstring(xml_str)


def get_dict_from_xml_element(xml_element: Element) -> dict:
    d = defaultdict(list)
    for item in xml_element:
        for sub_item in item:
            d[item.get("time")].append(dict(sub_item.items()))
    return d
