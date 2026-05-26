from datetime import datetime, timezone

from matches.models import Match, Participant, Player


def ingest_match(match_data, platform, rank=None):
    info = match_data["info"]
    match_id = match_data["metadata"]["matchId"]
    participants_data = info["participants"]

    puuids = [p["puuid"] for p in participants_data]
    existing_players = {p.puuid: p for p in Player.objects.filter(puuid__in=puuids)}

    players_to_create = []
    players_to_update = []

    for p in participants_data:
        puuid = p["puuid"]

        if puuid in existing_players:
            player = existing_players[puuid]
            player.platform = platform
            players_to_update.append(player)
        else:
            players_to_create.append(Player(puuid=puuid, platform=platform))

    Player.objects.bulk_create(players_to_create, ignore_conflicts=True)
    Player.objects.bulk_update(players_to_update, ["platform"])

    all_players = {p.puuid: p for p in Player.objects.filter(puuid__in=puuids)}

    match, _ = Match.objects.update_or_create(
        match_id=match_id,
        defaults={
            "game_creation": datetime.fromtimestamp(info["gameCreation"] / 1000, tz=timezone.utc),
            "game_duration": info["gameDuration"],
            "queue_id": info["queueId"],
            "platform": platform,
            "game_version": info.get("gameVersion"),
            "rank": rank,
        }
    )

    Participant.objects.filter(match=match).delete()

    Participant.objects.bulk_create([
        Participant(
            match=match,
            player=all_players[p["puuid"]],
            champion=p["championName"],
            win=p["win"],
            kills=p["kills"],
            deaths=p["deaths"],
            assists=p["assists"],
            item0=p.get("item0") or None,
            item1=p.get("item1") or None,
            item2=p.get("item2") or None,
            item3=p.get("item3") or None,
            item4=p.get("item4") or None,
            item5=p.get("item5") or None,
            item6=p.get("item6") or None,
        )
        for p in participants_data
    ])
