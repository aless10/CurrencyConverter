
from convert_app.cache.cache_utils import build_key_from_request


def test_build_key_from_request():
    request_body = {"key_1": "value_1", "key_2": "value_2", "key_3": None}
    key_result = build_key_from_request(request_body)
    assert isinstance(key_result, str)
    assert key_result == 'eb7870ac9a1a5df45731d8b7efcf1709'
