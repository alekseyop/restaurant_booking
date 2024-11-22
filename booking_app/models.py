from datetime import datetime, timedelta

from django.db import models

from accounts.models import User

NULLABLE = {'null': True, 'blank': True}


class Table(models.Model):
    number = models.CharField(max_length=10, verbose_name='Номер столика')
    seats = models.IntegerField(**NULLABLE, verbose_name='Количество мест')

    def __str__(self):
        return f"Столик {self.number} (мест: {self.seats})"

    def is_available(self):
        """
        Проверяет, доступен ли столик на указанную дату и время.
        """
        current_dt = datetime.now()
        bookings = Booking.objects.filter(table=self, date=current_dt.date())

        for booking in bookings:
            start_time = datetime.combine(booking.date, booking.time)
            end_time = start_time + timedelta(hours=booking.duration_hours)

            if start_time <= current_dt < end_time:
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

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Клиент')
    table = models.ForeignKey(Table, on_delete=models.CASCADE, verbose_name='Стол')
    date = models.DateField(verbose_name='Дата бронирования')
    time = models.TimeField(verbose_name='Время бронирования')
    guests = models.IntegerField(verbose_name='Количество гостей')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Дата создания')
    duration_hours = models.IntegerField(default=1, verbose_name='Продолжительность брони в часах')  # Продолжительность брони в часах

    def __str__(self):
        return f"Бронирование столика {self.table.number} на {self.date} {self.time}"