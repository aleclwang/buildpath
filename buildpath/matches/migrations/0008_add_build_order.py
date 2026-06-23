from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0007_add_indexes'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='build_order',
            field=models.JSONField(default=list),
        ),
    ]
