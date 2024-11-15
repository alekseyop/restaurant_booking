from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Booking
from .forms import BookingForm
from .forms import RegistrationForm


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


def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BookingForm()
    return render(request, 'booking_app/booking.html', {'form': form})


def profile(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking_app/profile.html', {'bookings': bookings})


def contacts(request):
    return render(request, 'booking_app/contacts.html')
