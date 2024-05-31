from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from .views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include('api.urls', namespace='api')),
    path('dev/', include('dev.urls', namespace='dev')),
    path('account/', include('account.urls', namespace='account')),
]

urlpatterns += static(settings.STATIC_URL , document_root=settings.STATIC_ROOT)