from django.db.models import Count, Max, F
from django.shortcuts import render, get_object_or_404
from league_tracker.models import User, Records, Decks, Event
from league_tracker.forms import UserForm, DeckForm, RecordForm, EventForm
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
    ### When somebody puts in a result we want to put in the reverse as well
    ### for example: user 3 sweeps user 1, we want to include a result for
    ### user 3 - user 1 6-0 points
    ### user 1 - user 3 0-6 points
    if request.method == 'POST':
        form = RecordForm(request.POST)
        reverse_form = request.POST.copy()
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
        form.save()
        form = RecordForm(reverse_form)
        form.save()
        return HttpResponseRedirect('/')
    else:
        form = RecordForm()
    return render(request, 'add_records.html', {'form': form})

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
    sos = Records.objects.sos(id)
    esos = Records.objects.esos(id)
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
    sos = Records.objects.sos(id, current_night)
    esos = Records.objects.esos(id, current_night)
    user = User.objects.get(pk=id)
    context = {
            'records': records,
            'user': user,
            'sos': sos,
            'esos': esos,
            }
    return render(request, 'standings.html', context)

def all_records(request, game_night=None):
    records = Records.objects.annotate(odd=F('pk') % 2).filter(odd=True)
    print(records.values())
    return HttpResponseRedirect('/')
