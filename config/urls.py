from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("booking_app.urls", namespace="booking_app")),  # Главная и другие страницы бронирования
    path("", include("accounts.urls", namespace="accounts")),
]

# Подключение статических и медиа файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
