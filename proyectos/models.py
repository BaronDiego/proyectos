import datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Base(models.Model):
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    uc = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario que Crea")
    um = models.IntegerField(blank=True, null=True, verbose_name="Usuario que modifica")

    class Meta:
        abstract = True


ESTADO = (
    ('EJ', 'En ejecución'),
    ('F', 'Finalizado'),
    ('S', 'Suspendido'),
    ('C', 'Cancelado'),
)

TERMINAL = (
    ('BUN', 'Buenaventura'),
    ('CTG', 'Cartagena'),
    ('BOG', 'Bogotá'),
    ('GLB', 'Global'),
)

class ProyectoMacro(Base):
    nombre = models.CharField(max_length=250)
    descripcion = models.TextField(verbose_name='Descripción')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    terminal = models.CharField(max_length=3, choices=TERMINAL)
    valor_proyecto = models.BigIntegerField(default=0, blank=True, null=True)
    valor_proyecto_planeado = models.BigIntegerField(default=0, blank=True, null=True, verbose_name='Costo Planeado')
    estado = models.CharField(max_length=2, choices=ESTADO)
    programado = models.FloatField(max_length=5, blank=True, null=True)
    avance = models.FloatField(max_length=5, blank=True, null=True)
    class Meta:
        ordering = ['-creado']

    def __str__(self):
        self.nombre = self.nombre.upper()
        return self.nombre

    def duracion(self):
        duracion = self.fecha_fin - self.fecha_inicio
        return duracion.days

class Proyecto(Base):
    proyecto_macro = models.ForeignKey(ProyectoMacro, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=250)
    objeto = models.TextField()
    contratista = models.CharField(max_length=150)
    numero_contrato = models.CharField(max_length=150,verbose_name="Número Contrato")
    estado = models.CharField(max_length=2, choices=ESTADO)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    terminal = models.CharField(max_length=3, choices=TERMINAL)
    valor_proyecto = models.BigIntegerField(default=0, blank=True, null=True)
    valor_proyecto_planeado = models.BigIntegerField(default=0, blank=True, null=True, verbose_name='Costo Planeado')
    programado = models.FloatField(max_length=5, blank=True, null=True)
    avance = models.FloatField(max_length=5, blank=True, null=True)
    responsable = models.CharField(max_length=50, blank=True)
    interventoria = models.BooleanField(default=False)

    class Meta:
        ordering = ['-creado']

    def __str__(self):
        return self.nombre

    def duracion(self):
        duracion = self.fecha_fin - self.fecha_inicio
        return duracion.days


class Pago(Base):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    fecha_pago = models.DateField()
    valor_pago = models.IntegerField(blank=True, null=True)
    concepto_pago = models.CharField(max_length=150)
    numero_factura = models.CharField(max_length=15, blank=True)
    class Meta:
        ordering = ['-creado']


class Documento(Base):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)
    documento = models.FileField(upload_to='documentos/%Y/%m/%d/')
    uc = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario que Crea")
    um = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['-creado']


class Imagen(Base):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)
    imagen = models.ImageField(upload_to='imagenes/%Y/%m/%d/')
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    uc = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario que Crea")
    um = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['-creado']


class Cambio(Base):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=150)
    afecta_tiempo = models.BooleanField(default=False, verbose_name="Afecta en Tiempo")
    duracion = models.IntegerField(blank=True, null=True)
    afecta_costo = models.BooleanField(default=False, verbose_name="Afecta en Costo")
    costo = models.IntegerField(blank=True, null=True)
    fecha_de_cambio = models.DateField()
    genero_documento = models.BooleanField(default=False)
    nombre_documento = models.CharField(max_length=150)

    class Meta:
        ordering = ['-creado']


class Actividad(Base):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    actualizado = models.DateTimeField(auto_now=True)
    programado = models.FloatField(max_length=5, blank=True, null=True)
    avance = models.FloatField(max_length=5, blank=True, null=True)

    class Meta:
        ordering = ['creado']

    def __str__(self):
        return self.nombre

    def duracion(self):
        duracion = (self.fecha_fin - self.fecha_inicio) + datetime.timedelta(days=1)
        return duracion.days

    
class BibliotecaProyecto(Base):
    nombre = models.CharField(max_length=150)
    cotizaciones = models.IntegerField(blank=True, null=True)
    area = models.CharField(max_length=100, verbose_name="Área")
    impacto = models.TextField()
    presupuesto =models.IntegerField(blank=True, null=True)
    documento = models.FileField(upload_to='bibliotecap/%Y/%m/%d/', blank=True)
    
    class Meta:
        ordering = ['-creado']

    def __str__(self):
        return self.nombre


class ActividadMacro(Base):
    proyecto = models.ForeignKey(ProyectoMacro, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    actualizado = models.DateTimeField(auto_now=True)
    programado = models.FloatField(max_length=5, blank=True, null=True)
    avance = models.FloatField(max_length=5, blank=True, null=True)

    class Meta:
        ordering = ['creado']

    def __str__(self):
        return self.nombre

    def duracion(self):
        duracion = (self.fecha_fin - self.fecha_inicio) + datetime.timedelta(days=1)
        return duracion.days


class DocumentoMacro(Base):
    proyecto = models.ForeignKey(ProyectoMacro, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)
    documento = models.FileField(upload_to='documentos/macro/%Y/%m/%d/')

    class Meta:
        ordering = ['-creado']

class Comentarios(Base):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='comentarios')
    comentarios = models.TextField()
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ('-creado',)