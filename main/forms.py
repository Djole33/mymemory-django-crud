from django import forms
from .models import Guess, Level

class WordForm(forms.ModelForm):
    class Meta:
        model = Guess
        fields = ('guess',)
        widgets = {
            'guess': forms.TextInput(attrs={'class': 'form-control'}),
        }

class LevelForm(forms.Form):
    LEVEL_CHOICES = [(i, f'Level {i} ({i+1} words)') for i in range(1, 21)]
    level = forms.ChoiceField(choices=LEVEL_CHOICES, label="Select Level")