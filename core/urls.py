from django.urls import path, include
from .views import ani_ctg, capex_bun, lote_e_bun,home, HomeSinPrevilegios

urlpatterns = [
    path('index/', home, name='home'),
    path('capex_bun/', capex_bun, name='capex_bun'),
    path('ani/', ani_ctg, name='ani_ctg'),
    path('lote_e_bun/', lote_e_bun, name='lote_e'),
    path('', include('django.contrib.auth.urls')),
    path('sin_privilegios/', HomeSinPrevilegios.as_view(), name='sin_privilegios')
]