from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from league_tracker.models import User, Records, Decks
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
    if request.method == 'POST':
        form = RecordForm(request.POST)
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

