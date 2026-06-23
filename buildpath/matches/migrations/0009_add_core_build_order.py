from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0008_add_build_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='core_build_order',
            field=models.JSONField(default=list),
        ),
    ]
