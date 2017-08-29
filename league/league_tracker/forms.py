from django import forms
from django.core.exceptions import ValidationError
from league_tracker.models import User, Decks, Records

class UserForm(forms.ModelForm):
   class Meta:
       model = User
       fields = ['name']

class DeckForm(forms.ModelForm):
    class Meta:
        model = Decks
        fields = '__all__'

class RecordForm(forms.ModelForm):
    class Meta:
        model = Records
        fields = '__all__'
