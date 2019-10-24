from argparse import Namespace
from unittest import mock
from lxml import etree

from convert_app.xml_data.importer import get_data_from_url, get_xml_from_string, serialize_from_xml_element


@mock.patch("convert_app.xml_data.importer.requests")
def test_get_data_from_url(mock_request):
    url = "http://mock_url.xml"
    mock_request.get.return_value = Namespace(content='<?xml version="1.0"?><response/>')
    result = get_data_from_url(url)
    assert result == '<?xml version="1.0"?><response/>'


def test_get_xml_from_string():
    xml_str = '<?xml version="1.0"?><response/>'
    result = get_xml_from_string(xml_str)
    assert isinstance(result, etree._Element)


def test_serialize_from_xml_element():
    e = etree.fromstring('<Cube>'
                         '  <Cube time="2019-10-22">'
                         '      <Cube currency="USD" rate="1.113"/>'
                         '      <Cube currency="JPY" rate="120.87"/>'
                         '  </Cube>'
                         '  <Cube time="2019-10-23">'
                         '      <Cube currency="BGN" rate="1.9558"/>'
                         '      <Cube currency="CZK" rate="25.57"/>'
                         '  </Cube>'
                         '</Cube>')
    d = serialize_from_xml_element(e)
    assert d == [
        {"time": "2019-10-22", "values": [
            {"currency": "USD", "rate": "1.113"},
            {"currency": "JPY", "rate": "120.87"}
        ]},
        {"time": "2019-10-23", "values": [
            {"currency": "BGN", "rate": "1.9558"},
            {"currency": "CZK", "rate": "25.57"}
        ]}
    ]
