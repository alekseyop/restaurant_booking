from django import forms
from django.core.exceptions import ValidationError
from django.utils.timezone import make_aware, is_naive

from booking_app.models import Booking

from datetime import datetime, timedelta


class BookingForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={"type": "time"}))
    duration_hours = forms.IntegerField(min_value=1, max_value=12, label="Продолжительность (в часах)")

    class Meta:
        model = Booking
        fields = ["table", "guests", "date", "time", "duration_hours"]

    def clean(self):
        cleaned_data = super().clean()

        # Список полей для проверки
        required_fields = ["table", "date", "time", "duration_hours"]

        # Проверяем, что все поля заполнены
        if not all(cleaned_data.get(field) for field in required_fields):
            return cleaned_data

        # Извлечение значений
        table = cleaned_data.get("table")
        date = cleaned_data.get("date")
        time = cleaned_data.get("time")
        duration_hours = cleaned_data.get("duration_hours")

        # Преобразуем дату и время в datetime
        start_time = datetime.combine(date, time)

        # Преобразуем в offset-aware, если требуется
        if is_naive(start_time):
            start_time = make_aware(start_time)

        # Рассчитываем время окончания брони
        end_time = start_time + timedelta(hours=duration_hours)

        # Проверяем пересечение с другими бронями
        overlapping_bookings = Booking.objects.filter(
            table=table,
            date=date,
        )

        for booking in overlapping_bookings:
            existing_start_time = datetime.combine(booking.date, booking.time)
            existing_end_time = existing_start_time + timedelta(hours=booking.duration_hours)

            # Преобразуем в offset-aware, если требуется
            if is_naive(existing_start_time):
                existing_start_time = make_aware(existing_start_time)
            if is_naive(existing_end_time):
                existing_end_time = make_aware(existing_end_time)

            # Проверяем пересечение интервалов
            if not (end_time <= existing_start_time or start_time >= existing_end_time):
                raise ValidationError("Этот столик уже забронирован на указанное время.")

        # Проверяем, что бронирование не в прошлом
        current_dt = datetime.now()
        if is_naive(current_dt):
            current_dt = make_aware(current_dt)
        if start_time < current_dt:
            raise ValidationError("Нельзя забронировать на прошедшее время.")

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
