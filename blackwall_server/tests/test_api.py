from requests import get


def test_home_page():
    """Test the health status"""
    assert get('http://localhost:5000/health', timeout=15).status_code == 200
    print("Test is successful")
