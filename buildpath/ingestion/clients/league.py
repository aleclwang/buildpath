from .base import request, get_url

def get_league_entries(host, tier, division, page):
    return request(
        get_url(host, f"/lol/league/v4/entries/RANKED_SOLO_5x5/{tier}/{division}"),
        params={"page": page}
    )

APEX_TIER_PATHS = {
    "MASTER": "masterleagues",
    "GRANDMASTER": "grandmasterleagues",
    "CHALLENGER": "challengerleagues",
}

def get_apex_league(host, tier):
    path = APEX_TIER_PATHS[tier.upper()]
    response = request(get_url(host, f"/lol/league/v4/{path}/by-queue/RANKED_SOLO_5x5"))
    return response["entries"]

def get_rank_by_puuid(host, puuid):
    entries = request(get_url(host, f"/lol/league/v4/entries/by-puuid/{puuid}"))
    for entry in entries:
        if entry["queueType"] == "RANKED_SOLO_5x5":
            return entry
    return None