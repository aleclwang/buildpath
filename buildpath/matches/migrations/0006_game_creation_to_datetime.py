from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0005_add_match_game_version'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql="ALTER TABLE matches_match ALTER COLUMN game_creation TYPE timestamp with time zone USING to_timestamp(game_creation / 1000.0);",
                    reverse_sql=migrations.RunSQL.noop,
                ),
            ],
            state_operations=[
                migrations.AlterField(
                    model_name='match',
                    name='game_creation',
                    field=models.DateTimeField(),
                ),
            ],
        ),
    ]
