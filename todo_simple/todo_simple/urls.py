from django.contrib import admin
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
	path('admin/', admin.site.urls),
	path('', include('todo_simple_app.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
