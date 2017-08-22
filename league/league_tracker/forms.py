from django import forms
from django.core.exceptions import ValidationError
from league_tracker.models import User, League, Decks, Records

class UserForm(forms.ModelForm):
   class Meta:
       model = User
       fields = ['name']

class LeagueForm(forms.ModelForm):
    class Meta:
        model = League
        fields = ['league_name']

class DeckForm(forms.ModelForm):
    class Meta:
        model = Decks
        fields = '__all__'

class RecordForm(forms.ModelForm):
    class Meta:
        model = Records
        fields = '__all__'
