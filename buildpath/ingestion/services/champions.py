from champions.models import Champion
from ingestion.clients.ddragon import get_champions


def sync_champions():
    version, data = get_champions()

    existing = {c.riot_id: c for c in Champion.objects.all()}

    to_create = []
    to_update = []

    for riot_id, payload in data.items():
        defaults = {
            "key": int(payload["key"]),
            "name": payload["name"],
            "title": payload["title"],
            "tags": payload.get("tags", []),
            "partype": payload.get("partype", ""),
            "icon": f"https://ddragon.leagueoflegends.com/cdn/{version}/img/champion/{payload['image']['full']}",
        }

        if riot_id in existing:
            champion = existing[riot_id]
            for k, v in defaults.items():
                setattr(champion, k, v)
            to_update.append(champion)
        else:
            to_create.append(Champion(riot_id=riot_id, **defaults))

    Champion.objects.bulk_create(to_create, ignore_conflicts=True)
    Champion.objects.bulk_update(to_update, defaults.keys())
