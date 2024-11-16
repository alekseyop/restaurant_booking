from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Страницы аутентификации
    # path('register/', views.register, name='register'),
    # path('login/', auth_views.LoginView.as_view(template_name='booking_app/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Страницы личного кабинета
    path('profile/', views.profile, name='profile'),
    path('booking/edit/<int:pk>/', views.edit_booking, name='edit_booking'),
    path('booking/cancel/<int:pk>/', views.cancel_booking, name='cancel_booking'),

    path('', views.home, name='home'),  #главная страница
    path('about/', views.about, name='about'),  #О нас
    path('booking/', views.booking_view, name='booking'),
    # path('booking/', views.booking, name='booking'), #Страница бронирования
    path('profile/', views.profile, name='profile'),  #Страница личного кабинета
    path('contacts/', views.contacts, name='contacts'),  # Страница с контактами
    path('available-tables/', views.available_tables, name='available_tables'),
    path('book-table/<int:table_id>/', views.book_table, name='book_table'),
]