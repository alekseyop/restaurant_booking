from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils import timezone
from django.utils.timezone import now

from .models import Booking, Table
from .forms import BookingForm
from .forms import RegistrationForm
from datetime import timedelta, datetime
from django.db.models import Q

from dateutil.parser import parse


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('profile')
    else:
        form = RegistrationForm()
    return render(request, 'booking_app/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'booking_app/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


# User = get_user_model()


@login_required(login_url='login')  # Замените 'login' на имя URL для страницы входа
def profile(request):
    user = request.user  # Получаем текущего пользователя
    # Передаем пользователя в шаблон профиля
    return render(request, 'accounts/profile.html', {'user': user})


# @login_required
# def profile(request):
#     if request.user.is_authenticated:
#         bookings = Booking.objects.filter(user=request.user).order_by('-date', '-time')
#         return render(request, 'booking_app/profile.html', {'bookings': bookings})
#     else:
#         return redirect('login')

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Перенаправляем на логин, если пользователь не авторизован

    user = request.user
    bookings = user.booking_set.all()

    return render(request, 'profile.html', {
        'user': user,
        'bookings': bookings,
    })


@login_required
def edit_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = BookingForm(instance=booking)
    return render(request, 'booking_app/edit_booking.html', {'form': form, 'booking': booking})


@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if request.method == 'POST':
        booking.status = 'canceled'
        booking.save()
        return redirect('profile')
    return render(request, 'booking_app/cancel_booking.html', {'booking': booking})


def home(request):
    return render(request, 'booking_app/home.html')


def about(request):
    return render(request, 'booking_app/about.html')


# def booking(request):
#     if request.method == 'POST':
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = BookingForm()
#     return render(request, 'booking_app/booking.html', {'form': form})
def booking_view(request):
    user = request.user
    date = request.GET.get('date', datetime.now().date())
    time = request.GET.get('time', datetime.now().strftime('%H:%M'))
    duration = int(request.GET.get('duration', 1))

    booking_start = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    booking_end = booking_start + timedelta(hours=duration)

    tables = Table.objects.all()
    table_statuses = []

    for table in tables:
        overlapping_bookings = Booking.objects.filter(
            table=table,
            date=booking_start.date(),
            time__lt=booking_end.time(),
        ).exclude(
            time__gte=(booking_start + timedelta(
                hours=table.booking_set.first().duration_hours if table.booking_set.first() else 0
            )).time()
        )

        is_free = not overlapping_bookings.exists()
        if table.number:  # Убедимся, что `number` не None
            table_statuses.append({'table': table, 'is_free': is_free})
        else:
            print(f"Столик {table.number} не имеет ID!")

    context = {
        'user': user,
        'date': date,
        'time': time,
        'duration': duration,
        'table_statuses': table_statuses,
    }
    return render(request, 'booking_app/booking.html', context)


def profile(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking_app/profile.html', {'bookings': bookings})


def contacts(request):
    return render(request, 'booking_app/contacts.html')


def available_tables(request):
    # Получаем дату и время из запроса
    date_str = request.GET.get('date', None)
    time_str = request.GET.get('time', None)

    # Парсим дату и время
    if date_str and time_str:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        time = datetime.strptime(time_str, '%H:%M').time()
    else:
        date = timezone.now().date()
        time = timezone.now().time()

    # Формируем список столиков с их статусами
    tables = Table.objects.all()
    table_statuses = []
    for table in tables:
        bookings = Booking.objects.filter(table=table, date=date)
        is_free = True
        for booking in bookings:
            start_time = datetime.combine(booking.date, booking.time)
            end_time = start_time + timedelta(hours=booking.duration_hours)
            requested_time = datetime.combine(date, time)
            if start_time <= requested_time < end_time:
                is_free = False
                break
        table_statuses.append({
            'table': table,
            'is_free': is_free,
        })

    context = {
        'table_statuses': table_statuses,
        'date': date,
        'time': time,
    }
    return render(request, 'booking_app/available_tables.html', context)


def parse_date_auto(date_str):
    # Удаляем 'г.'
    date_str = date_str.replace(' г.', '')

    # Словарь для преобразования месяцев
    month_translation = {
        'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4,
        'мая': 5, 'июня': 6, 'июля': 7, 'августа': 8,
        'сентября': 9, 'октября': 10, 'ноября': 11, 'декабря': 12
    }

    # Разбиваем строку
    try:
        day, month_name, year = date_str.split(' ')
        month = month_translation[month_name]
        return datetime(int(year), month, int(day)).date()
    except (ValueError, KeyError):
        raise ValueError(f"Неверный формат даты: {date_str}")


from django.utils.timezone import make_aware, now
from datetime import datetime


def book_table(request, table_id):
    table = Table.objects.get(number=table_id)  # Получаем объект столика
    date_str = request.GET.get('date', None)
    time_str = request.GET.get('time', None)

    # Парсим дату и время
    if date_str and time_str:
        try:
            date = parse_date_auto(date_str)
            time = datetime.strptime(time_str, '%H:%M').time()
        except ValueError:
            return render(request, 'booking_app/error.html', {
                'error_message': "Неверный формат даты или времени."
            })
    else:
        date = now().date()
        time = now().time()

    # Объединяем дату и время в один объект datetime
    booking_datetime = datetime.combine(date, time)

    # Приводим booking_datetime к aware datetime
    booking_datetime = make_aware(booking_datetime)

    # Проверяем, что время бронирования в будущем
    if booking_datetime + timedelta(hours=1) <= now():
        return render(request, 'booking_app/error.html', {
            'error_message': "Дата и время бронирования должны быть в будущем."
        })

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.table = table
            booking.date = date
            booking.time = time
            booking.save()
            return redirect('available_tables')
    else:
        form = BookingForm()

    context = {
        'form': form,
        'table': table,
        'date': date,
        'time': time,
    }
    return render(request, 'booking_app/book_table.html', context)
