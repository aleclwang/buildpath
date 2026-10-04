from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0002_natural_pks'),
    ]

    operations = [
        # 0002 already dropped the id column in SQL; this only syncs migration state.
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.RemoveField(
                    model_name='item',
                    name='id',
                ),
            ],
        ),
    ]
