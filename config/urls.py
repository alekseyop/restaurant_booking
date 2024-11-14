from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Админка Django
    path('admin/', admin.site.urls),

    # Маршруты для приложения бронирования
    path('', include('booking_app.urls')),  # Главная и другие страницы бронирования

    # Маршруты для управления пользователями
    path('accounts/', include('accounts.urls')),  # Профиль, регистрация, авторизация

    # # Стандартные маршруты аутентификации Django
    # path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('register/', include('accounts.urls')),  # Регистрация пользователя
]

# Подключение статических и медиа файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
