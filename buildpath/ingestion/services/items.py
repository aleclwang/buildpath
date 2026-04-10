from items.models import Item
from ingestion.clients.ddragon import get_latest_version, get_items, get_icon_url

def sync_items():
    version = get_latest_version()
    data = get_items(version)

    existing = {i.riot_id: i for i in Item.objects.all()}

    to_create = []
    to_update = []

    for riot_id, payload in data.items():
        riot_id = int(riot_id)

        defaults = {
            "name": payload.get("name", "Item not found"),
            "description": payload.get("description", ""),
            "plaintext": payload.get("plaintext", ""),
            
            "from_items": payload.get("from", []),
            "into_items": payload.get("to", []),

            "icon": get_icon_url(version, payload.get("image", {"full": "1001.png"})["full"]),

            "gold_base": payload.get("gold", {"base": 0, "purchasable": True, "total": 0, "sell": 0})["base"],
            "purchasable": payload.get("gold", {"base": 0, "purchasable": True, "total": 0, "sell": 0})["purchasable"],
            "gold_total": payload.get("gold", {"base": 0, "purchasable": True, "total": 0, "sell": 0})["total"],
            "gold_sell": payload.get("gold", {"base": 0, "purchasable": True, "total": 0, "sell": 0})["sell"],
        
            "tags": payload.get("tags", []),
            "maps": payload.get("maps", []),
            "stats": payload.get("stats", []),

            "depth": payload.get("depth", 1),

        }

        if riot_id in existing:
            item = existing[riot_id]
            for k, v in defaults.items():
                setattr(item, k, v)
            to_update.append(item)
        else:
            to_create.append(Item(riot_id=riot_id, **defaults))

    Item.objects.bulk_create(to_create, ignore_conflicts=True)
    Item.objects.bulk_update(to_update, defaults.keys())