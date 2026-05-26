from .base import request

def get_latest_version():
    return request("https://ddragon.leagueoflegends.com/api/versions.json")[0]


def get_items(version):
    url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/item.json"
    return request(url)["data"]

def get_icon_url(version, filename):
    return f"https://ddragon.leagueoflegends.com/cdn/{version}/img/item/{filename}"