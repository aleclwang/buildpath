from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests
import os

API_KEY = os.getenv("API_KEY")


class VerboseRetry(Retry):
    def increment(self, method=None, url=None, response=None, error=None, _pool=None, _stacktrace=None):
        if response and response.status == 429:
            retry_after = response.headers.get("Retry-After", "unknown")
            print(f"[rate limit] Rate limited. Waiting {retry_after}s...")
        return super().increment(method, url, response, error, _pool, _stacktrace)


def create_session():
    retry = VerboseRetry(
        total=20,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        respect_retry_after_header=True,
    )

    adapter = HTTPAdapter(max_retries=retry)

    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    return session


session = create_session()
session.headers.update({
    "X-Riot-Token": API_KEY
})

def get_url(host, path):
    return f"https://{host}.api.riotgames.com{path}"
def request(url, params=None):
    response = session.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()