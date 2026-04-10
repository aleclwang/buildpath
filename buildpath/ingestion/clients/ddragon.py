from .base import fetch_json

def get_latest_version():
    return fetch_json("https://ddragon.leagueoflegends.com/api/versions.json")[0]


def get_items(version):
    url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/item.json"
    return fetch_json(url)["data"]

def get_icon_url(version, filename):
    return f"https://ddragon.leagueoflegends.com/cdn/{version}/img/item/{filename}"