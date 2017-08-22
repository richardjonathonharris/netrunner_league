from django.db import models

# Create your models here.

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    def __str__(self):
        return self.name

class League(models.Model):
    league_id = models.AutoField(primary_key=True)
    league_name = models.CharField(max_length=100, default='New League')
    def __str__(self):
        return self.league_name

class Decks(models.Model):
    SIDES = (
            ('R', 'Runner'),
            ('C', 'Corporation')
            )
    FACTIONS = (
            ('H', 'Haas-Bioroid'),
            ('J', 'Jinteki'),
            ('W', 'Weyland'),
            ('N', 'NBN'),
            ('A', 'Anarch'),
            ('S', 'Shaper'),
            ('C', 'Criminal'),
            ('P', 'Apex'),
            ('D', 'Adam'),
            ('L', 'Sunny Lebeau')
            )
    deck_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User) 
    deck_name = models.CharField(max_length=250)
    side = models.CharField(max_length=1, choices=SIDES)
    faction = models.CharField(max_length=1, choices=FACTIONS)
    league = models.ForeignKey(League)

class Records(models.Model):
    WIN_LOSE = (
            ('W', 'Win'),
            ('L', 'Lose')
            )
    user_id = models.ForeignKey(User, related_name='+')
    opponent_id = models.ForeignKey(User, related_name='+')
    status = models.CharField(max_length=1, choices=WIN_LOSE)
    points_win = models.IntegerField()
    points_lose = models.IntegerField()
    flatline = models.BooleanField()
    league = models.ForeignKey(League)


