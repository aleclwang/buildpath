import random
from collections import deque
from datetime import timedelta

from django.utils import timezone

from ingestion.clients.league import get_league_entries, get_rank_by_puuid
from ingestion.clients.match import get_match, get_match_ids
from ingestion.services.matches import ingest_match
from matches.models import Match, Player

PLATFORM_TO_REGION = {
    "na1": "americas",
    "br1": "americas",
    "la1": "americas",
    "la2": "americas",
    "euw1": "europe",
    "eun1": "europe",
    "tr1": "europe",
    "ru": "europe",
    "kr": "asia",
    "jp1": "asia",
    "oc1": "sea",
}

RECHECK_THRESHOLD = timedelta(days=7)


def _rank_from_participants(platform, match_data):
    participants = match_data["info"]["participants"][:]
    random.shuffle(participants)
    for p in participants:
        entry = get_rank_by_puuid(platform, p["puuid"])
        if entry:
            return entry["tier"]
    return None


def run_seed(platform, tier, division, max_players=None):
    region = PLATFORM_TO_REGION[platform.lower()]

    seed_page = random.randint(1, 10)
    print(f"[seed] Fetching seed players from page {seed_page} of {tier} {division}...")
    entries = get_league_entries(platform, tier, division, seed_page)

    seed_data = {e["puuid"]: e for e in entries}
    seed_puuids = list(seed_data.keys())
    random.shuffle(seed_puuids)
    print(f"[seed] Seeding with {len(seed_puuids)} players")

    Player.objects.bulk_create([
        Player(puuid=puuid, platform=platform)
        for puuid in seed_puuids
    ], ignore_conflicts=True)

    player_queue = deque(seed_puuids)
    seen_puuids = set(seed_puuids)
    players_processed = 0

    while player_queue:
        puuid = player_queue.popleft()
        now = timezone.now()

        player = Player.objects.filter(puuid=puuid).first()
        if player and player.last_checked and (now - player.last_checked) < RECHECK_THRESHOLD:
            print(f"[seed] Skipping {puuid[:16]}... (recently checked)")
            continue

        is_seed = puuid in seed_data
        seed_rank = seed_data[puuid]["tier"] if is_seed else None

        match_ids = get_match_ids(region, puuid)
        players_processed += 1
        existing = set(Match.objects.filter(match_id__in=match_ids).values_list("match_id", flat=True))
        print(f"[seed] Player {players_processed} ({puuid[:16]}...): {len(match_ids)} matches found ({len(existing)} already ingested) | queue: {len(player_queue)} | seen: {len(seen_puuids)}")

        for match_id in match_ids:
            if match_id in existing:
                continue
            try:
                print(f"[seed]   Ingesting {match_id}...")
                match_data = get_match(region, match_id)

                rank = seed_rank if is_seed else _rank_from_participants(platform, match_data)
                ingest_match(match_data, platform, rank=rank)

                for p in match_data["info"]["participants"]:
                    new_puuid = p["puuid"]
                    if new_puuid not in seen_puuids:
                        seen_puuids.add(new_puuid)
                        player_queue.append(new_puuid)
            except Exception as e:
                print(f"[seed]   ERROR ingesting {match_id}: {e}")

        Player.objects.filter(puuid=puuid).update(last_checked=now)

        if max_players and len(seen_puuids) >= max_players:
            print(f"[seed] Reached max_players limit ({max_players}), stopping.")
            break
