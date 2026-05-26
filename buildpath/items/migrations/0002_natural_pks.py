from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql=[
                        # Drop unique constraint on riot_id
                        """
                        DO $$
                        DECLARE r RECORD;
                        BEGIN
                            FOR r IN
                                SELECT tc.constraint_name
                                FROM information_schema.table_constraints tc
                                JOIN information_schema.key_column_usage kcu
                                    ON tc.constraint_name = kcu.constraint_name
                                WHERE tc.table_name = 'items_item'
                                  AND tc.constraint_type = 'UNIQUE'
                                  AND kcu.column_name = 'riot_id'
                            LOOP
                                EXECUTE 'ALTER TABLE items_item DROP CONSTRAINT ' || r.constraint_name;
                            END LOOP;
                        END $$;
                        """,
                        "ALTER TABLE items_item DROP CONSTRAINT items_item_pkey;",
                        "ALTER TABLE items_item DROP COLUMN id;",
                        "ALTER TABLE items_item ADD PRIMARY KEY (riot_id);",
                    ],
                    reverse_sql=migrations.RunSQL.noop,
                ),
            ],
            state_operations=[
                migrations.AlterField(
                    model_name='item',
                    name='riot_id',
                    field=models.IntegerField(primary_key=True, serialize=False),
                ),
            ],
        ),
    ]
