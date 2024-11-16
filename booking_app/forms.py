from django import forms
from .models import Booking
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class BookingForm(forms.ModelForm):
    booking_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    booking_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    duration_hours = forms.IntegerField(min_value=1, max_value=12, label="Продолжительность (в часах)")

    class Meta:
        model = Booking
        fields = ['booking_date', 'booking_time', 'duration_hours']


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
