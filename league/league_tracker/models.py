from django.db import models
from django.utils.functional import cached_property
from django.template.defaultfilters import slugify
import requests

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    is_bye = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.name

class Decks(models.Model):
    deck_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True) 
    game = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    runner_id = models.CharField(max_length=250, null=True)
    runner_faction = models.CharField(max_length=250, null=True)
    corp_id = models.CharField(max_length=250, null=True)
    corp_faction = models.CharField(max_length=250, null=True)

class StatsManager(models.Manager):
    def sos(self, user_id, event_id=None): # note we need to figure out a way to exclude BYEs
        if not event_id:
            own_records = self.filter(user_id_id=user_id)
            opponents = [rec.opponent_id_id for rec in own_records]
            opponents_records = self.filter(user_id_id__in=opponents).exclude(opponent_id_id=user_id)
        else:
            own_records = self.filter(user_id_id=user_id).filter(game_id=event_id)
            opponents = [rec.opponent_id_id for rec in own_records]
            opponents_records = self.filter(user_id_id__in=opponents).filter(game_id=event_id).exclude(opponent_id_id=user_id)
        denom = 0
        num = 0
        for opponent in opponents:
            runner_results = list(opponents_records.filter(user_id_id=opponent).values_list('runner_status', flat=True))
            corp_results = list(opponents_records.filter(user_id_id=opponent).values_list('corp_status', flat=True))
            points = 0
            for result in [runner_results, corp_results]:
                points += sum([3 for item in result if item == 'WI']) 
                if opponent == 21:
                    print(result) # ok SOS is borked here. What's going on?
                points += sum([2 for item in result if item == 'TW'])
                points += sum([1 for item in result if item == 'TI'])
            if user_id == 17:
                print('opponent: {}, points: {}'.format(opponent, points))
            if len(runner_results) == 0:
                points /= 1
            else:
                points /= len(runner_results)
            denom += points
            num += 1
        return denom/num

    def esos(self, user_id, event_id=None):
        own_records = self.filter(user_id_id=user_id)
        opponents = [rec.opponent_id_id for rec in own_records]
        opp_sos = [self.sos(opp) for opp in opponents]
        return sum(opp_sos)/len(opp_sos)
    
    def total_points(self, user_id):
        own_records = self.filter(user_id_id=user_id)
        runner_results = list(own_records.values_list('runner_status', flat=True))
        corp_results = list(own_records.values_list('corp_status', flat=True))
        points = 0
        for result in [runner_results, corp_results]:
            points += sum([3 for item in result if item == 'WI']) 
            points += sum([2 for item in result if item == 'TW'])
            points += sum([1 for item in result if item == 'TI'])
        return points

class Records(models.Model):
    WIN_LOSE = (
            ('WI', 'Win'),
            ('TW', 'Timed Win'),
            ('TL', 'Timed Loss'),
            ('LO', 'Lose'),
            ('TI', 'Tie'),
            )
    choices = [(i, i) for i in range(1, 16)]
    user_id = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    opponent_id = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    corp_status = models.CharField(max_length=2, choices=WIN_LOSE, null=True, default='WI')
    runner_status = models.CharField(max_length=2, choices=WIN_LOSE, null=True, default='WI')
    game = models.ForeignKey(Event, related_name='+', null=True, blank=True, on_delete=models.CASCADE)
    deck = models.ForeignKey(Decks, on_delete=models.CASCADE, null=True)
    round_num = models.IntegerField(null=True, default=1, choices=choices)
    display = models.BooleanField(default=True)
    linked_record = models.IntegerField(null=True, default=1)
    objects = models.Manager()
    stats = StatsManager()
