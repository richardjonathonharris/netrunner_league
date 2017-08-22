from django.shortcuts import render
from league_tracker.models import User, Records, Decks, League
from league_tracker.forms import UserForm, LeagueForm, DeckForm, RecordForm
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.

def index(request): 
    all_user = User.objects.all()
    all_record = Records.objects.all()
    all_deck = Decks.objects.all()
    all_league = League.objects.all()
    context = {
            'user': all_user,
            'record': all_record,
            'deck': all_deck,
            'league': all_league,
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

def create_league(request):
    if request.method == 'POST':
        form = LeagueForm(request.POST)
        form.save()
        return HttpResponseRedirect('/')
    else:
        form = LeagueForm()
    return render(request, 'add_league.html', {'form': form})

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
