from django.db import models

# Create your models here.
class Item(models.Model):
    riot_id = models.IntegerField(unique=True)

    name = models.CharField(max_length=255)
    description = models.TextField()
    plaintext = models.TextField()

    from_items = models.JSONField(default=list)
    into_items = models.JSONField(default=list)

    icon = models.URLField()

    gold_base = models.IntegerField()
    purchasable = models.BooleanField()
    gold_total = models.IntegerField()
    gold_sell = models.IntegerField()
    
    tags = models.JSONField(default=list)
    maps = models.JSONField(default=dict)
    stats = models.JSONField(default=dict)

    depth = models.IntegerField()

    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name