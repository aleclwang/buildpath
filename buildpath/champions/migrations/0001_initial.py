from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Champion',
            fields=[
                ('riot_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('key', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=150)),
                ('tags', models.JSONField(default=list)),
                ('partype', models.CharField(max_length=50)),
                ('icon', models.URLField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
