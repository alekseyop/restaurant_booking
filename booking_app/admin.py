from django.contrib import admin
from .models import Table, Booking

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'seats')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'table', 'date', 'time', 'guests', 'created_at')
    list_filter = ('date', 'time')
    search_fields = ('user__username', 'table__number')
