from django.contrib import admin
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
	path('', include('TODOapps.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
