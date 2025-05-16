from requests import get

def test_api_health():
    assert get('http://localhost:5000', timeout=15).status_code == 200
