from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/', include('api.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:      # если проект в режиме Дебаг, то директории для медиафайлов здесь
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
