from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from accounts.views import UserCreateView, UserDetailView
from accounts.apps import AccountsConfig

app_name = AccountsConfig.name

urlpatterns = [
    path('profile/login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('profile/logout/', LogoutView.as_view(), name='logout'),
    path('profile/register/', UserCreateView.as_view(), name='register'),
    path('profile/<int:pk>/', UserDetailView.as_view(), name='profile'),
]