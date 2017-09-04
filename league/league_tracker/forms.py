from django import forms
from django.core.exceptions import ValidationError
from league_tracker.models import User, Decks, Records, Event

class UserForm(forms.ModelForm):
   class Meta:
       model = User
       fields = ['name']

class DeckForm(forms.ModelForm):
    class Meta:
        model = Decks
        fields = '__all__'

class RecordForm(forms.ModelForm):
    user_id = forms.ModelChoiceField(queryset=User.objects, empty_label=None)
    opponent_id = forms.ModelChoiceField(queryset=User.objects, empty_label=None)
    game = forms.ModelChoiceField(queryset=Event.objects.order_by('-date'), empty_label=None)
    class Meta:
        model = Records
        fields = ['user_id', 'opponent_id', 'corp_status',
                'runner_status', 'game', 'round_num']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
