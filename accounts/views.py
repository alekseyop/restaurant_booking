from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from accounts.forms import CustomUserCreationForm
from accounts.models import User
from booking_app.models import Booking


class UserCreateView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("accounts:login")


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bookings"] = Booking.objects.filter(owner=self.object).order_by("date", "time")
        return context
