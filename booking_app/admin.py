from django.contrib import admin
from booking_app.models import Table, Booking


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'seats')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('table', 'date', 'time', 'guests', 'created_at')
    list_filter = ('date', 'time')
    search_fields = ('table__number',)
