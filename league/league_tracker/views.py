from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from league_tracker.models import User, Records, Decks
from league_tracker.forms import UserForm, DeckForm, RecordForm
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.

def index(request): 
    all_user = User.objects.all()
    all_record = Records.objects.all()
    all_deck = Decks.objects.all()
    context = {
            'user': all_user,
            'record': all_record,
            'deck': all_deck,
            }
    return render(request, 'index.html', context)

def thanks(request):
    return HttpResponse('<b>Thanks!</b>')

def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        form.save()
        return HttpResponseRedirect('/thanks/')
    else:
        form = UserForm()
    return render(request, 'add_user.html', {'form': form})

def create_deck(request):
    if request.method == 'POST':
        form = DeckForm(request.POST)
        form.save()
        return HttpResponseRedirect('/')
    else:
        form = DeckForm()
    return render(request, 'add_decks.html', {'form': form})

def create_record(request):
    if request.method == 'POST':
        form = RecordForm(request.POST)
        form.save()
        return HttpResponseRedirect('/')
    else:
        form = RecordForm()
    return render(request, 'add_records.html', {'form': form})

def return_all_standings(request):
    all_records = Records.objects.all()
    context = {
            'record': all_record,
            }
    return render(request, 'index.html', context)

def records(request, id):
    records = Records.objects.filter(user_id_id=id)
    user = User.objects.get(pk=id)
    grouped = records.values('opponent_id', 'status').annotate(dcount=Count('opponent_id'))
    opponents = [item['opponent_id'] for item in grouped]
    opp_records = Records.objects.filter(user_id_id__in=opponents)
    results = {}
    for opp in opponents:
        results[opp] = {}
        for rec in opp_records:
            if rec.user_id_id != opp:
                pass
            elif rec.opponent_id_id not in results[opp].keys():
                results[opp][rec.opponent_id_id] = []
                results[opp][rec.opponent_id_id].append(rec.status)
            else:
                results[opp][rec.opponent_id_id].append(rec.status)
    num_opponents = len(results)
    denom = 0
    numer = 0
    for opp in results.items():
        points = 0
        matches_played = 0
        for match in opp[1].items():
            points += sum([3 for item in match[1] if item == 'W'])
            matches_played += 1
        numer += (points / matches_played)
        denom += 1
    strength_of_schedule = numer / denom
    context = {
            'sos': strength_of_schedule,
            'records': records,
            'user': user
            }
    return render(request, 'standings.html', context)

