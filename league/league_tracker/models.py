from django.db import models
from django.utils.functional import cached_property
from django.template.defaultfilters import slugify

# Create your models here.

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    def __str__(self):
        return self.name

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

class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.name

class SoSManager(models.Manager):
    def sos(self, user_id, event_id=None): # need to add in filtering by event
        own_records = self.filter(user_id_id=user_id)
        opponents = [rec.opponent_id_id for rec in own_records]
        opponents_records = self.filter(user_id_id__in=opponents).exclude(opponent_id_id=user_id)
        denom = 0
        num = 0
        for opponent in opponents:
            runner_results = list(opponents_records.filter(user_id_id=opponent).values_list('runner_status', flat=True))
            corp_results = list(opponents_records.filter(user_id_id=opponent).values_list('corp_status', flat=True))
            points = 0
            for result in [runner_results, corp_results]:
                points += sum([3 for item in result if item == 'WI']) 
                points += sum([2 for item in result if item == 'TW'])
                points += sum([1 for item in result if item == 'TI'])
            points /= len(runner_results)
            denom += points
            num += 1
        return denom/num

    def esos(self, user_id, event_id=None):
        own_records = self.filter(user_id_id=user_id)
        opponents = [rec.opponent_id_id for rec in own_records]
        opp_sos = [self.sos(opp) for opp in opponents]
        return sum(opp_sos)/len(opp_sos)

class Records(models.Model):
    WIN_LOSE = (
            ('WI', 'Win'),
            ('TW', 'Timed Win'),
            ('TL', 'Timed Loss'),
            ('LO', 'Lose'),
            ('TI', 'Tie'),
            )
    user_id = models.ForeignKey(User, related_name='+')
    opponent_id = models.ForeignKey(User, related_name='+')
    corp_status = models.CharField(max_length=2, choices=WIN_LOSE, null=True)
    runner_status = models.CharField(max_length=2, choices=WIN_LOSE, null=True)
    game = models.ForeignKey(Event, related_name='+', null=True, blank=True)
    round_num = models.IntegerField(null=True)
    objects = SoSManager()
