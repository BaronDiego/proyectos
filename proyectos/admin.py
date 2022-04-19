from django.contrib import admin
from .models import Proyecto, Pago, Documento, Imagen, Cambio, Actividad

# Register your models here.
admin.site.site_header = "Administración AppGranel"

@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'contratista', 'numero_contrato', 'estado', 'terminal', 'fecha_inicio', 'fecha_fin' ,'creado', 'actualizado', 'uc', 'um']


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ['proyecto', 'valor_pago', 'fecha_pago', 'numero_factura','concepto_pago','creado', 'actualizado', 'uc', 'um']


@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ['proyecto', 'nombre', 'documento','creado', 'uc', 'um']


@admin.register(Imagen)
class ImagenAdmin(admin.ModelAdmin):
    list_display = ['proyecto', 'nombre', 'imagen','creado', 'uc', 'um']


@admin.register(Cambio)
class CambioAdmin(admin.ModelAdmin):
    list_display = ['proyecto', 'tipo', 'afecta_tiempo', 'duracion', 'afecta_costo', 'costo', 'fecha_de_cambio', 'genero_documento', 'nombre_documento', 'uc', 'um']


@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ['proyecto', 'nombre', 'fecha_inicio', 'fecha_fin','programado', 'avance', 'creado', 'uc', 'um']
