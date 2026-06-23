from django.core.management.base import BaseCommand
from matches.models import Participant
from ingestion.services.timelines import get_core_item_ids


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        core_ids = get_core_item_ids()
        print(f"[core_builds] {len(core_ids)} core item IDs loaded")

        qs = Participant.objects.exclude(build_order=[]).only("id", "build_order", "core_build_order")
        total = qs.count()
        print(f"[core_builds] {total} participants to backfill")

        batch = []
        for i, p in enumerate(qs.iterator(chunk_size=1000), start=1):
            p.core_build_order = [item_id for item_id in p.build_order if item_id in core_ids]
            batch.append(p)
            if len(batch) == 1000:
                Participant.objects.bulk_update(batch, ["core_build_order"])
                print(f"[core_builds] {i}/{total}")
                batch = []

        if batch:
            Participant.objects.bulk_update(batch, ["core_build_order"])
            print(f"[core_builds] {total}/{total}")

        print("[core_builds] done")
