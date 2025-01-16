from django import forms
from .models import *
from django.utils.timezone import now

class BookingCreateForm(forms.ModelForm):
    class Meta:
        model = FlightBooking
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        total_bookings = FlightBooking.objects.count()
        self.fields['reference_number'].initial = str(total_bookings + 1) # key of instance = number of entries + 1
        self.fields['reference_number'].disabled = True  
        self.fields['booking_date'].initial = now().date()
        self.fields['booking_date'].disabled = True
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.save()
        return instance
