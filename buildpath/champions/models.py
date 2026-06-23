from django.db import models


class Champion(models.Model):
    riot_id = models.CharField(max_length=50, primary_key=True)
    key = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=150)
    tags = models.JSONField(default=list)
    partype = models.CharField(max_length=50)
    icon = models.URLField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
