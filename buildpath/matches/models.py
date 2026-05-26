from django.db import models

# Create your models here.
class Player(models.Model):
    puuid = models.CharField(max_length=100, primary_key=True)
    platform = models.CharField(max_length=10)

    last_checked = models.DateTimeField(null=True)

class Match(models.Model):
    match_id = models.CharField(max_length=50, primary_key=True)

    game_creation = models.DateTimeField(db_index=True)
    game_duration = models.IntegerField()

    queue_id = models.IntegerField()
    platform = models.CharField(max_length=10, null=True)
    game_version = models.CharField(max_length=30, null=True)
    rank = models.CharField(max_length=20, null=True, db_index=True)

class Participant(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, db_column="puuid")

    champion = models.CharField(max_length=50, db_index=True)
    win = models.BooleanField()

    kills = models.IntegerField()
    deaths = models.IntegerField()
    assists = models.IntegerField()

    item0 = models.IntegerField(null=True)
    item1 = models.IntegerField(null=True)
    item2 = models.IntegerField(null=True)
    item3 = models.IntegerField(null=True)
    item4 = models.IntegerField(null=True)
    item5 = models.IntegerField(null=True)
    item6 = models.IntegerField(null=True)