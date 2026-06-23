from ingestion.clients.match import get_timeline
from items.models import Item
from matches.models import Participant


def get_core_item_ids():
    return set(
        Item.objects.filter(into_items=[], gold_total__gte=2200).values_list("riot_id", flat=True)
    )


def ingest_timeline(match_id, region):
    timeline = get_timeline(region, match_id)
    info = timeline["info"]

    id_to_puuid = {p["participantId"]: p["puuid"] for p in info["participants"]}
    core_ids = get_core_item_ids()

    build_orders = {}
    for frame in info["frames"]:
        for event in frame["events"]:
            if event["type"] == "ITEM_PURCHASED":
                puuid = id_to_puuid.get(event["participantId"])
                if puuid is not None:
                    build_orders.setdefault(puuid, []).append(event["itemId"])

    participants = {
        p.player_id: p
        for p in Participant.objects.filter(match_id=match_id).only("id", "player_id", "build_order", "core_build_order")
    }

    for puuid, order in build_orders.items():
        if puuid in participants:
            participants[puuid].build_order = order
            participants[puuid].core_build_order = [i for i in order if i in core_ids]

    Participant.objects.bulk_update(participants.values(), ["build_order", "core_build_order"])
