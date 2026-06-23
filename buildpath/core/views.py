from collections import Counter

from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count
from champions.models import Champion
from matches.models import Participant
from items.models import Item

RANK_TIERS = {
    "EMERALD+": ["EMERALD", "DIAMOND", "MASTER", "GRANDMASTER", "CHALLENGER"],
    "MASTER+":  ["MASTER", "GRANDMASTER", "CHALLENGER"],
}


def index(request):
    return render(request, "core/index.html")


def champions_api(request):
    names = list(Champion.objects.order_by("name").values_list("name", flat=True))
    return JsonResponse(names, safe=False)


def participants_api(request):
    champion = request.GET.get("champion", "").strip()
    rank_range = request.GET.get("rank", "").strip()

    if not champion or rank_range not in RANK_TIERS:
        return JsonResponse({"error": "champion and rank are required"}, status=400)

    tiers = RANK_TIERS[rank_range]
    qs = Participant.objects.filter(
        champion=champion,
        match__rank__in=tiers,
    ).values(
        "win", "kills", "deaths", "assists",
        "item0", "item1", "item2", "item3", "item4", "item5", "item6",
        "match__rank",
    )

    return JsonResponse(list(qs), safe=False)


def item_frequencies_api(request):
    champion = request.GET.get("champion", "").strip()
    rank_range = request.GET.get("rank", "").strip()

    if not champion:
        return JsonResponse({"error": "champion is required"}, status=400)

    slot = int(request.GET.get("slot", 0))
    path = [int(x) for x in request.GET.get("path", "").split(",") if x]

    qs = Participant.objects.filter(champion=champion)
    if rank_range in RANK_TIERS:
        qs = qs.filter(match__rank__in=RANK_TIERS[rank_range])

    counts = {}
    wins = {}
    for order, win in qs.values_list("core_build_order", "win"):
        if len(order) <= slot:
            continue
        if any(i >= len(order) or order[i] != path[i] for i in range(len(path))):
            continue
        item_id = order[slot]
        counts[item_id] = counts.get(item_id, 0) + 1
        wins[item_id] = wins.get(item_id, 0) + (1 if win else 0)

    item_ids = list(counts)
    icons = {i.riot_id: i.icon for i in Item.objects.filter(riot_id__in=item_ids)}

    result = sorted(
        [
            {
                "item_id": item_id,
                "icon": icons[item_id],
                "count": counts[item_id],
                "winrate": round(wins[item_id] / counts[item_id] * 100, 2),
            }
            for item_id in item_ids
            if item_id in icons
        ],
        key=lambda x: x["count"],
        reverse=True,
    )
    return JsonResponse(result, safe=False)
