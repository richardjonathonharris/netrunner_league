from django.db.models import Count, Max, F
from django.shortcuts import render, get_object_or_404
from league_tracker.models import User, Records, Decks, Event
from league_tracker.forms import UserForm, DeckForm, RecordForm, EventForm, get_faction_dictionary 
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
        runner_vals, corp_vals = get_faction_dictionary()
        payload = request.POST.copy()
        form = DeckForm(payload)
        form.save()
        updater = Decks.objects.last()
        updater.runner_faction = runner_vals[payload['runner_id']]
        updater.corp_faction = corp_vals[payload['corp_id']]
        updater.save()
        return HttpResponseRedirect('/')
    else:
        form = DeckForm()
    return render(request, 'add_decks.html', {'form': form})

def create_record(request):
    ### When somebody puts in a result we want to put in  reverse as well
    ### for example: user 3 sweeps user 1, we want to include a result for
    ### user 3 - user 1 6-0 points
    ### user 1 - user 3 0-6 points
    if request.method == 'POST':
        form = RecordForm(request.POST)
        reverse_form = request.POST.copy()
        original_form = request.POST.copy()
        form.save()
        reverse_form['opponent_id'] = request.POST['user_id']
        reverse_form['user_id'] = request.POST['opponent_id']
        flip_dict = {
                'WI': 'LO',
                'LO': 'WI',
                'TW': 'TL',
                'TL': 'TW',
                'TI': 'TI',
                }
        for stat in ['runner_status', 'corp_status']:
            reverse_form[stat] = flip_dict[request.POST[stat]]
        reverse_form['display'] = False
        form = RecordForm(reverse_form)
        form.save()
        opp_record = Records.objects.last()
        opp_record.linked_record = opp_record.pk - 1
        opp_record.save()
        user_record = Records.objects.get(pk=opp_record.pk-1)
        user_record.linked_record = user_record.pk + 1
        user_record.save()
        return HttpResponseRedirect('/')
    else:
        form = RecordForm()
    return render(request, 'add_records.html', {'form': form})

def update_record(request, id):
    record = Records.objects.get(pk=id)
    form = RecordForm(request.POST or None, instance=record)
    if request.method == 'POST':
        form.save()
        linked_record = Records.objects.get(pk=record.linked_record)
        updated_record = Records.objects.get(pk=id)
        linked_record.user_id = updated_record.opponent_id
        linked_record.opponent_id = updated_record.user_id
        linked_record.game = updated_record.game
        linked_record.round_num = updated_record.round_num
        flip_dict = {
                'WI': 'LO',
                'LO': 'WI',
                'TW': 'TL',
                'TL': 'TW',
                'TI': 'TI',
                }
        linked_record.runner_status = flip_dict[updated_record.runner_status]
        linked_record.corp_status = flip_dict[updated_record.corp_status]
        linked_record.save()
        return HttpResponseRedirect('/')
    return render(request, 'update_records.html', {'form': form, 'id': id})

def delete_record(request, id):
    record = Records.objects.filter(id=id)
    partner = record[0].linked_record
    Records.objects.filter(id=id).delete()
    Records.objects.filter(id=partner).delete()
    return HttpResponseRedirect('/')
    

def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        form.save()
        return HttpResponseRedirect('/')
    else:
        form = EventForm()
    return render(request, 'add_event.html', {'form': form})


def return_all_standings(request):
    all_records = Records.objects.all()
    context = {
            'record': all_record,
            }
    return render(request, 'index.html', context)

def records(request, id):
    records = Records.objects.filter(user_id_id=id)
    sos = Records.stats.sos(id)
    esos = Records.stats.esos(id)
    user = User.objects.get(pk=id)
    context = {
            'records': records,
            'user': user,
            'sos': sos,
            'esos': esos,
            }
    return render(request, 'standings.html', context)

def current_records(request, id):
    current_night = Event.objects.all().aggregate(Max('pk'))['pk__max']
    records = Records.objects.filter(user_id_id=id).filter(game_id=current_night)
    sos = Records.stats.sos(id, current_night)
    esos = Records.stats.esos(id, current_night)
    user = User.objects.get(pk=id)
    context = {
            'records': records,
            'user': user,
            'sos': sos,
            'esos': esos,
            }
    return render(request, 'standings.html', context)

def all_records(request, game_night=None):
    records = Records.objects.filter(display=True)
    non_filtered_records = Records.objects.all()
    all_decks = Decks.objects.all()
    all_players = set(list(Records.objects.values_list('user_id_id', flat=True)))
    stats = {}
    for player in all_players:
        ids = all_decks.filter(user_id=player)
        # Ok, here's where we're leaving it!
        print(ids.values())
        stats[player] = {
                'name': User.objects.filter(user_id=player).values('name')[0]['name'],
                'points': Records.stats.total_points(player),
                'sos': Records.stats.sos(player),
                'esos': Records.stats.esos(player),
                }
    runner_records = non_filtered_records.values('runner_status').annotate(runner_count=Count('runner_status')).order_by('-runner_status')
    corp_records = non_filtered_records.values('corp_status').annotate(corp_count=Count('corp_status')).order_by('-corp_status')
    runner = [record for record in runner_records]
    corp = [record for record in corp_records]
    win_rates = {}
    for x in range(len(runner)):
        newkey = runner[x]['runner_status']
        win_rates[newkey] = {
                'runner': runner[x].get('runner_count', 0),
                'corp': corp[x].get('corp_count', 0),
                }
    for key in ['WI', 'LO', 'TW', 'TL', 'TI']:
        if not win_rates.get(key, None):
            win_rates[key] = {
                    'runner': 0,
                    'corp': 0
                    }
    context = {
            'records': records,
            'stats': stats,
            'win_rates': win_rates,
            }
    return render(request, 'records.html', context)
