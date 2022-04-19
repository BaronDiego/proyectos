from django import forms
from .models import Proyecto, Pago, Documento, Imagen, Cambio, Actividad, BibliotecaProyecto, ProyectoMacro, ActividadMacro, DocumentoMacro, Comentarios

class ProyectoMacroForm(forms.ModelForm):
    class Meta:
        model = ProyectoMacro
        exclude = ['uc', 'um', 'creado', 'actualizado']

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['proyecto_macro', 'nombre', 'objeto', 'contratista', 'numero_contrato', 'valor_proyecto_planeado','valor_proyecto','estado', 'fecha_inicio', 'fecha_fin', 'responsable', 'interventoria','terminal', 'programado', 'avance']
        widgets = {
            'fecha_inicio':forms.DateInput(attrs={'placeholder':'dd/mm/aaaa'}),
            'fecha_fin':forms.DateInput(attrs={'placeholder':'dd/mm/aaaa'})
        }


class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['valor_pago', 'fecha_pago', 'numero_factura','concepto_pago']
        widgets = {
            'fecha_pago':forms.DateInput(attrs={'placeholder':'dd/mm/aaaa'}),
        }


class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['nombre', 'documento']


class ImagenForm(forms.ModelForm):
    class Meta:
        model = Imagen
        fields = ['nombre', 'imagen']


class CambioForm(forms.ModelForm):
    class Meta:
        model = Cambio
        fields = ['tipo', 'afecta_tiempo', 'duracion', 'afecta_costo', 'costo', 'fecha_de_cambio', 'genero_documento', 'nombre_documento']
        widgets = {
            'fecha_de_cambio':forms.DateInput(attrs={'placeholder':'dd/mm/aaaa'})
        }


class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['nombre', 'fecha_inicio', 'fecha_fin','programado', 'avance']
        widgets = {
            'fecha_inicio':forms.DateInput(attrs={'placeholder':'dd/mm/aaaa'}),
            'fecha_fin':forms.DateInput(attrs={'placeholder':'dd/mm/aaaa'})
        }


class BibliotecaPryectoForm(forms.ModelForm):
    class Meta:
        model = BibliotecaProyecto
        exclude = ['creado', 'actualizado','uc', 'um']


class ActividadMacroForm(forms.ModelForm):
    class Meta:
        model = ActividadMacro
        fields = ['proyecto', 'nombre', 'fecha_inicio', 'fecha_fin','programado', 'avance']
        widgets = {
            'fecha_inicio':forms.DateInput(attrs={'placeholder':'dd/mm/aaaa'}),
            'fecha_fin':forms.DateInput(attrs={'placeholder':'dd/mm/aaaa'})
        }


class DocumentoMacroForm(forms.ModelForm):
    class Meta:
        model = DocumentoMacro
        fields = ['proyecto', 'nombre', 'documento']
        # widgets = {
        #     'documento':forms.FileInput(),
        # }


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentarios
        fields = ['comentarios']