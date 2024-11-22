from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import CreateView, TemplateView, DetailView
from django.urls import reverse_lazy, reverse

from booking_app.forms import BookingForm
from booking_app.models import Booking, Table

from datetime import datetime


class HomeView(TemplateView):
    template_name = "booking/home.html"


class AboutView(TemplateView):
    template_name = "booking/about.html"


class BookingCreateView(CreateView):
    model = Booking
    form_class = BookingForm
    template_name = "booking/booking_form.html"
    success_url = reverse_lazy("booking_app:booking_create")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tables"] = Table.objects.all()
        return context

    def form_valid(self, form):
        booking = form.save(commit=False)
        user = self.request.user
        booking.owner = user
        return super().form_valid(form)


class TableDetailVew(LoginRequiredMixin, DetailView):
    model = Table
    template_name = "booking/table_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bookings"] = Booking.objects.filter(table=self.object, date__gte=datetime.now()).order_by(
            "date", "time"
        )
        return context


def confirm(request, pk):

    booking = Booking.objects.get(pk=pk)
    if request.GET.get("confirm") == "True":
        booking.status = "confirmed"
    else:
        booking.status = "canceled"
    booking.save()

    return redirect("accounts:profile", request.user.id)
