from django import forms
from django.forms import ModelForm
from .models import Score


class ScoreForm(ModelForm):
    class Meta:
        model = Score
        fields = ["number_of_tries"]

        
