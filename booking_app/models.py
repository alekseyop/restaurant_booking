from datetime import datetime, timedelta

from django.conf import settings
from django.db import models
from accounts.models import User
from django.core.exceptions import ValidationError

NULLABLE = {'null': True, 'blank': True}


class Table(models.Model):
    number = models.CharField(max_length=10, verbose_name='Номер столика')
    seats = models.IntegerField(**NULLABLE, verbose_name='Количество мест')

    def __str__(self):
        return f"Столик {self.number} (мест: {self.seats})"

    def is_available(self, date, time):
        """
        Проверяет, доступен ли столик на указанную дату и время.
        """
        bookings = Booking.objects.filter(
            table=self,
            booking_date=date
        )
        for booking in bookings:
            start_time = datetime.combine(booking.date, booking.time)
            end_time = start_time + timedelta(hours=booking.duration_hours)

            # Если текущее время пересекается с бронью
            requested_time = datetime.combine(date, time)
            if start_time <= requested_time < end_time:
                return False
        return True

    class Meta:
        verbose_name = 'Столик'
        verbose_name_plural = 'Столики'


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('confirmed', 'Подтверждено'),
        ('canceled', 'Отменено'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date = models.DateField(verbose_name='Дата бронирования')
    time = models.TimeField(verbose_name='Время бронирования')
    guests = models.IntegerField(verbose_name='Количество гостей')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Дата создания')
    duration_hours = models.IntegerField(default=1, verbose_name='Продолжительность брони в часах')  # Продолжительность брони в часах

    def __str__(self):
        return f"Бронирование столика {self.table.number} для {self.user.username} на {self.date} {self.time}"

    def clean(self):
        # Проверяем на пересечение бронирования
        bookings = Booking.objects.filter(
            table=self.table,
            booking_date=self.date
        )
        new_start = datetime.combine(self.date, self.time)
        new_end = new_start + timedelta(hours=self.duration_hours)

        for booking in bookings:
            existing_start = datetime.combine(booking.date, booking.time)
            existing_end = existing_start + timedelta(hours=booking.duration_hours)
            if (new_start < existing_end and new_end > existing_start):
                raise ValidationError("Этот столик уже забронирован на выбранное время.")
    @classmethod
    def check_availability(cls, date, time, guests):
        """Проверка доступности столиков для определенного времени и количества гостей."""
        booked_tables = cls.objects.filter(date=date, time=time).values_list('table', flat=True)
        return Table.objects.exclude(id__in=booked_tables).filter(seats__gte=guests)
