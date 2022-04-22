from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views
from django.conf import settings
from django.conf.urls.static import static
from proyectos.views import graficos

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('', graficos, name="graficos"),
    path('proyectos/', include('proyectos.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

