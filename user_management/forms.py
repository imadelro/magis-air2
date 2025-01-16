from django import forms
from .models import *


class PassengerUpdateForm(forms.ModelForm):
    class Meta:
        model = Passenger
        exclude=['user']


class PassengerCreateForm(forms.ModelForm):
    class Meta:
        model = Passenger
        exclude=['user']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'})
        }
