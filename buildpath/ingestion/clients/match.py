from datetime import datetime, timedelta, timezone

from .base import request, get_url

def get_match(host, match_id):
    return request(get_url(host, f"/lol/match/v5/matches/{match_id}"))

def get_timeline(host, match_id):
    return request(get_url(host, f"/lol/match/v5/matches/{match_id}/timeline"))

def get_match_ids(host, puuid):
    start_time = int((datetime.now(timezone.utc) - timedelta(days=30)).timestamp())
    return request(
        get_url(host, f"/lol/match/v5/matches/by-puuid/{puuid}/ids"),
        params={
            "startTime": start_time,
            "queue": 420,
            "count": 100
        }
    )