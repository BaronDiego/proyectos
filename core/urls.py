from django.urls import path
from .views import home, HomeSinPrevilegios

urlpatterns = [
    path('index/', home, name='home'),
    path('sin_privilegios/', HomeSinPrevilegios.as_view(), name='sin_privilegios')
]