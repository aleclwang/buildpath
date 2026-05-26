from django.db import migrations


class Migration(migrations.Migration):
    """
    - Cleans up id fields from Match and Player in Django's state only
      (columns were already dropped from the DB in 0002_natural_pks)
    - Drops tier, division, summoner_name from Player (DB + state)
    """

    dependencies = [
        ('matches', '0002_natural_pks'),
    ]

    operations = [
        # id columns are already gone from the DB — update state only
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.RemoveField(model_name='match', name='id'),
                migrations.RemoveField(model_name='player', name='id'),
            ],
        ),

        # These columns exist in the DB and need to be dropped
        migrations.RemoveField(model_name='player', name='tier'),
        migrations.RemoveField(model_name='player', name='division'),
        migrations.RemoveField(model_name='player', name='summoner_name'),
    ]
