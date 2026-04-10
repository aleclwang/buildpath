from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests

def create_session():
    retry = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )

    adapter = HTTPAdapter(max_retries=retry)

    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    return session


session = create_session()

def fetch_json(url):
    response = session.get(url, timeout=10)
    response.raise_for_status()
    return response.json()