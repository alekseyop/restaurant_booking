from django.urls import path

from booking_app.views import HomeView, BookingCreateView, TableDetailVew, confirm
from booking_app.apps import BookingConfig

app_name = BookingConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('booking/create/', BookingCreateView.as_view(), name='booking_create'),
    path('booking/table/<int:pk>/', TableDetailVew.as_view(), name='booking_table'),
    path('booking/confirm/<int:pk>/', confirm, name='confirm')
]