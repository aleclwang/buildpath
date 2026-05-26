from django.core.management.base import BaseCommand

from matches.models import Match, Participant, Player


class Command(BaseCommand):
    help = "Delete all Match, Participant, and Player records"

    def handle(self, *args, **kwargs):
        p_count, _ = Participant.objects.all().delete()
        m_count, _ = Match.objects.all().delete()
        pl_count, _ = Player.objects.all().delete()

        self.stdout.write(self.style.SUCCESS(
            f"Deleted {p_count} participants, {m_count} matches, {pl_count} players."
        ))
