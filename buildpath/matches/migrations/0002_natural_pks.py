import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    atomic = False

    dependencies = [
        ('matches', '0001_initial'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql=[
                        # Step 1: Add temp columns to Participant
                        "ALTER TABLE matches_participant ADD COLUMN temp_match_id VARCHAR(50);",
                        "ALTER TABLE matches_participant ADD COLUMN temp_puuid VARCHAR(100);",

                        # Step 2: Populate temp columns from related tables
                        """
                        UPDATE matches_participant mp
                        SET temp_match_id = m.match_id
                        FROM matches_match m
                        WHERE mp.match_id = m.id;
                        """,
                        """
                        UPDATE matches_participant mp
                        SET temp_puuid = p.puuid
                        FROM matches_player p
                        WHERE mp.player_id = p.id;
                        """,

                        # Step 3: Drop FK constraints on Participant dynamically
                        """
                        DO $$
                        DECLARE r RECORD;
                        BEGIN
                            FOR r IN
                                SELECT tc.constraint_name
                                FROM information_schema.table_constraints tc
                                JOIN information_schema.key_column_usage kcu
                                    ON tc.constraint_name = kcu.constraint_name
                                WHERE tc.table_name = 'matches_participant'
                                  AND tc.constraint_type = 'FOREIGN KEY'
                                  AND kcu.column_name IN ('match_id', 'player_id')
                            LOOP
                                EXECUTE 'ALTER TABLE matches_participant DROP CONSTRAINT ' || r.constraint_name;
                            END LOOP;
                        END $$;
                        """,

                        # Step 4: Drop unique constraints on natural key columns
                        """
                        DO $$
                        DECLARE r RECORD;
                        BEGIN
                            FOR r IN
                                SELECT tc.constraint_name, tc.table_name
                                FROM information_schema.table_constraints tc
                                JOIN information_schema.key_column_usage kcu
                                    ON tc.constraint_name = kcu.constraint_name
                                WHERE tc.table_name IN ('matches_match', 'matches_player')
                                  AND tc.constraint_type = 'UNIQUE'
                                  AND kcu.column_name IN ('match_id', 'puuid')
                            LOOP
                                EXECUTE 'ALTER TABLE ' || r.table_name || ' DROP CONSTRAINT ' || r.constraint_name;
                            END LOOP;
                        END $$;
                        """,

                        # Step 5: Rebuild Match with natural PK
                        "ALTER TABLE matches_match DROP CONSTRAINT matches_match_pkey;",
                        "ALTER TABLE matches_match DROP COLUMN id;",
                        "ALTER TABLE matches_match ADD PRIMARY KEY (match_id);",

                        # Step 6: Rebuild Player with natural PK
                        "ALTER TABLE matches_player DROP CONSTRAINT matches_player_pkey;",
                        "ALTER TABLE matches_player DROP COLUMN id;",
                        "ALTER TABLE matches_player ADD PRIMARY KEY (puuid);",

                        # Step 7: Rebuild Participant FK columns
                        "ALTER TABLE matches_participant DROP COLUMN match_id;",
                        "ALTER TABLE matches_participant DROP COLUMN player_id;",
                        "ALTER TABLE matches_participant RENAME COLUMN temp_match_id TO match_id;",
                        "ALTER TABLE matches_participant RENAME COLUMN temp_puuid TO puuid;",

                        # Step 8: Re-add FK constraints
                        """
                        ALTER TABLE matches_participant
                            ADD CONSTRAINT matches_participant_match_id_fk
                            FOREIGN KEY (match_id) REFERENCES matches_match(match_id) ON DELETE CASCADE;
                        """,
                        """
                        ALTER TABLE matches_participant
                            ADD CONSTRAINT matches_participant_puuid_fk
                            FOREIGN KEY (puuid) REFERENCES matches_player(puuid) ON DELETE CASCADE;
                        """,
                    ],
                    reverse_sql=migrations.RunSQL.noop,
                ),
            ],
            state_operations=[
                migrations.AlterField(
                    model_name='match',
                    name='match_id',
                    field=models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                migrations.AlterField(
                    model_name='player',
                    name='puuid',
                    field=models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
                migrations.AlterField(
                    model_name='participant',
                    name='player',
                    field=models.ForeignKey(
                        db_column='puuid',
                        on_delete=django.db.models.deletion.CASCADE,
                        to='matches.player',
                    ),
                ),
            ],
        ),
    ]
