from django import forms
from django.core.exceptions import ValidationError

from booking_app.models import Booking

from datetime import datetime


class BookingForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={"type": "time"}))
    duration_hours = forms.IntegerField(min_value=1, max_value=12, label="Продолжительность (в часах)")

    class Meta:
        model = Booking
        fields = ["table", "guests", "date", "time", "duration_hours"]

    def clean(self):
        cleaned_data = super().clean()

        current_dt = datetime.now()
        start_time = datetime.combine(cleaned_data.get("date"), cleaned_data.get("time"))

        if current_dt > start_time:
            raise ValidationError("Нельзя забронировать на прошлое")

        return cleaned_data

    def clean_guests(self):
        guests_count = self.cleaned_data.get("guests")
        table = self.cleaned_data.get("table")
        if guests_count <= 0:
            raise ValidationError("Нельзя забронировать на 0 или меньше гостей")
        if guests_count > table.seats:
            raise ValidationError("Нельзя забронировать, недостаточно мест")
        return guests_count

    def clean_duration_hours(self):
        d_time = self.cleaned_data.get("duration_hours")
        if d_time <= 0:
            raise ValidationError("Нельзя забронировать на 0 или меньше часов")
        if d_time > 5:
            raise ValidationError("Нельзя забронировать больше чем на 5 часов")
        return d_time
