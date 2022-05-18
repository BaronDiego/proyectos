import datetime
import re
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from core.views import SinPrivilegios
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.db.models import Q
from django.core.mail import send_mail, EmailMessage
from .models import Costo, CurvaS, Imagen, Proyecto, Pago, Documento, Cambio, Actividad, BibliotecaProyecto, ProyectoMacro, ActividadMacro, DocumentoMacro
from .forms import CostosForm, CurvaForm, ProyectoForm, PagoForm, DocumentoForm, ImagenForm, CambioForm, ActividadForm, BibliotecaPryectoForm, ProyectoMacroForm, ActividadMacroForm, DocumentoMacroForm, ComentarioForm


############################
## Vistas Modelo Proyecto ##
############################
class ListaProyectos(SinPrivilegios, ListView):
    permission_required = "proyectos.view_proyecto"
    queryset = Proyecto.objects.filter(proyecto_macro=None)
    template_name = 'proyectos/proyecto/listado_proyectos.html'
    context_object_name = 'proyectos_list'


@login_required(login_url='login')
def detalle_proyecto(request, id):
    proyecto = get_object_or_404(Proyecto, id=id)
    nombre = proyecto.nombre
    comentarios = proyecto.comentarios.filter(activo=True)
    nuevo_comenatrio = None

    #### Crear Cometarios ####
    if request.method == 'POST':
        comentario_form = ComentarioForm(data=request.POST)
        if comentario_form.is_valid():
            nuevo_comenatrio = comentario_form.save(commit=False)
            nuevo_comenatrio.proyecto =proyecto
            comentario_form.instance.uc = request.user
            nuevo_comenatrio.save()
            send_mail(
                '¡Nuevo cometario en el proyecto {}!'.format(nombre), 
                'El usuario {} ha creado un nuevo comenatrio al proyecto {}\n\nNota: No responder a este correo, se envia automaticamente'.format(request.user, nombre), 
                'djangopruebas7@gmail.com', 
                ['diego.baron@algranel.com.co'], 
                fail_silently=False
            )
            messages.success(request, 'Comentario creado correctamente')
            return redirect('detalle_proyecto', id=id)
    else:
        comentario_form = ComentarioForm()

    ### Crear Pagos ###
    if request.method == 'POST':
        pago_form = PagoForm(data=request.POST)
        if pago_form.is_valid():
            nuevo_pago = pago_form.save(commit=False)
            nuevo_pago.proyecto = proyecto
            nuevo_pago.proyecto.um = request.user.id
            pago_form.instance.uc = request.user

            nuevo_pago.proyecto.save()
            nuevo_pago.save()
            messages.success(request, 'Pago creado correctamente')
            return redirect('detalle_proyecto', id=id)
    else:
        pago_form = PagoForm()


    ### Cargar Documento ###
    if request.method == 'POST':
        documento_form = DocumentoForm(request.POST, request.FILES)
        if documento_form.is_valid():
            nuevo_documento = documento_form.save(commit=False)
            nuevo_documento.proyecto = proyecto
            nuevo_documento.proyecto.um = request.user.id
            documento_form.instance.uc = request.user
            nuevo_documento.proyecto.save()
            nuevo_documento.save()
            messages.success(request, 'Documento creado correctamente')
            return redirect('detalle_proyecto', id=id)
    else:
        documento_form = DocumentoForm()

    
    ### Cargar Imágen ###
    if request.method == 'POST':
        imagen_form = ImagenForm(request.POST, request.FILES)
        if imagen_form.is_valid():
            nuevo_imagen = imagen_form.save(commit=False)
            nuevo_imagen.proyecto = proyecto
            nuevo_imagen.proyecto.um = request.user.id
            imagen_form.instance.uc = request.user
            nuevo_imagen.proyecto.save()
            nuevo_imagen.save()
            messages.success(request, 'Imagén creada correctamente')
            return redirect('detalle_proyecto', id=id)
    else:
        imagen_form = ImagenForm()


    ### Crear Control de Cambio ###
    if request.method == "POST":
        form_cambio = CambioForm(data=request.POST)
        if form_cambio.is_valid():
            cd = form_cambio.cleaned_data
            nuevo_control = form_cambio.save(commit=False)
            nuevo_control.proyecto = proyecto
            nuevo_control.proyecto.um = request.user.id
            costo = cd['costo']
            duracion = cd['duracion']

            if costo == None:
                nuevo_control.proyecto.valor_proyecto = nuevo_control.proyecto.valor_proyecto
            else:
                nuevo_control.proyecto.valor_proyecto = nuevo_control.proyecto.valor_proyecto + costo

            if duracion == None:
                nuevo_control.proyecto.fecha_fin = nuevo_control.proyecto.fecha_fin
            else:   
                nuevo_control.proyecto.fecha_fin = nuevo_control.proyecto.fecha_fin + datetime.timedelta(days=duracion)

            nuevo_control.proyecto.save()
            form_cambio.instance.uc = request.user
            form_cambio.save()
            messages.success(request, 'Cambio creado correctamente')
            return redirect('detalle_proyecto', id=id)
    else:
        form_cambio = CambioForm()

    
    ### Crear Actividades ###
    if request.method == 'POST':
        form_actividad = ActividadForm(data=request.POST)
        if form_actividad.is_valid():
            cd = form_actividad.cleaned_data
            nueva_actividad = form_actividad.save(commit=False)
            nueva_actividad.proyecto = proyecto
            nueva_actividad.proyecto.um = request.user.id
            form_actividad.instance.uc = request.user
            nueva_actividad.proyecto.save()
            nueva_actividad.save()
            messages.success(request, 'Actividad creada correctamente')
            return redirect('detalle_proyecto', id=id)
    else:
        form_actividad = ActividadForm()

    
    ### Crear Curva ###
    if request.method == 'POST':
        form_curva = CurvaForm(data=request.POST)
        if form_curva.is_valid():
            cd = form_curva.cleaned_data
            nueva_c = form_curva.save(commit=False)
            nueva_c.proyecto = proyecto
            nueva_c.proyecto.um = request.user.id
            form_curva.instance.uc = request.user
            nueva_c.proyecto.save()
            nueva_c.save()
            return redirect('detalle_proyecto', id=id)
    else:
        form_curva = CurvaForm()

    
    fechas =[]
    fechas1 = []
    lista_fechas_flat=[]
    programado = []
    programado_list_flat = []
    ejecutado = []
    ejecutado_list_flat = []
    for f in CurvaS.objects.filter(proyecto_id=id).values_list('fecha'):
        fechas.append(f)
    fechas_list = list(map(list,fechas))

    for i in fechas_list:
        lista_fechas_flat += i

    for f in lista_fechas_flat:
        fechas1.append(f.isoformat())

    for p in CurvaS.objects.filter(proyecto_id=id).values_list('programado'):
        programado.append(p)
    programado_list = list(map(list, programado))
    
    for i in programado_list:
        programado_list_flat += i

    for e in CurvaS.objects.filter(proyecto_id=id).values_list('avance'):
        if e != (0.1,):
            ejecutado.append(e)

    ejecutado_list = list(map(list, ejecutado))
    
    for i in ejecutado_list:
        ejecutado_list_flat += i

    duracion_c = Cambio.objects.filter(id=id)
    cambios = Cambio.objects.filter(proyecto_id=id)
    imagenes = Imagen.objects.filter(proyecto_id=id)
    actividades = Actividad.objects.filter(proyecto_id=id)


    ### Crear Gráfico Costos ###
    if request.method == 'POST':
        form_costo = CostosForm(data=request.POST)
        if form_costo.is_valid():
            cd = form_costo.cleaned_data
            nuevo_costo = form_costo.save(commit=False)
            nuevo_costo.proyecto = proyecto
            nuevo_costo.proyecto.um = request.user.id
            form_costo.instance.uc = request.user
            nuevo_costo.proyecto.save()
            nuevo_costo.save()
            return redirect('detalle_proyecto', id=id)
    else:
        form_costo = CostosForm()

    costo_programado = []
    costo_programado_list_flat = []
    costo_ejecutado = []
    costo_ejecutado_list_flat = []
    facturacion_planeada = []
    fp_list_flat = []
    facturacion_real = []
    fr_list_flat = []

    for f in Costo.objects.filter(proyecto_id=id).values_list('costo_programado'):
        costo_programado.append(f)
    costo_programado_list = list(map(list,costo_programado))

    for i in costo_programado_list:
        costo_programado_list_flat += i

    for f in Costo.objects.filter(proyecto_id=id).values_list('costo_ejecutado'):
        costo_ejecutado.append(f)
    costo_ejecutado_list = list(map(list,costo_ejecutado))

    for i in costo_ejecutado_list:
        costo_ejecutado_list_flat += i

    for f in Costo.objects.filter(proyecto_id=id).values_list('facturacion_planeada'):
        facturacion_planeada.append(f)
    fc_ejecutado_list = list(map(list,facturacion_planeada))

    for i in fc_ejecutado_list:
        fp_list_flat += i

    for f in Costo.objects.filter(proyecto_id=id).values_list('facturacion_real'):
        facturacion_real.append(f)
    fc_real_list = list(map(list,facturacion_real))

    for i in  fc_real_list:
       fr_list_flat += i

    costo_programado_list_flat += costo_ejecutado_list_flat
    costo_programado_list_flat += fp_list_flat
    costo_programado_list_flat += fr_list_flat

    try:
        costos = Costo.objects.all()
        costo_id = Costo.objects.filter(proyecto_id=id).values()
        id_costo = costo_id[0]['id']
    except IndexError:
        id_costo = None



    return render(request, 'proyectos/proyecto/proyecto_detalle.html', {
        'proyecto':proyecto, 
        'cambios':cambios,
        'imagenes':imagenes,
        'comentarios':comentarios,
        'nuevo_comentario':nuevo_comenatrio,
        'comentario_form':comentario_form,
        'pago_form':pago_form,
        'form_cambio':form_cambio,
        'imagen_form':imagen_form,
        'documento_form':documento_form,
        'form_actividad':form_actividad,
        'actividades':actividades,
        'form_curva':form_curva,
        'programado_list_flat':programado_list_flat,
        'fechas1':fechas1,
        'ejecutado_list_flat':ejecutado_list_flat,
        'form_costo':form_costo,
        'costo_programado_list_flat':costo_programado_list_flat,
        'costo_ejecutado_list_flat':costo_ejecutado_list_flat,
        'costos':costos,
        'id_costo':id_costo,
        })


class CrearProyecto( SuccessMessageMixin, SinPrivilegios, CreateView):
    permission_required = "proyectos.add_proyecto"
    model = Proyecto
    template_name = 'proyectos/proyecto/crear_proyecto.html'
    context_object_name = 'proyecto_create'
    form_class = ProyectoForm
    success_url = reverse_lazy('proyectos_list')
    success_message = "Proyecto creado correctamente"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)


class EditarProyecto(SuccessMessageMixin , SinPrivilegios, UpdateView):
    permission_required = "proyectos.change_proyecto"
    model = Proyecto
    template_name = 'proyectos/proyecto/editar_proyecto.html'
    context_object_name = 'proyecto_editar'
    form_class = ProyectoForm
    success_url = reverse_lazy('graficos')
    success_message = "Proyecto editado correctamente"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


class BorrarProyecto( SuccessMessageMixin, SinPrivilegios, DeleteView):
    permission_required = "proyectos.delete_proyecto"
    model = Proyecto
    template_name = 'proyectos/proyecto/borrar_proyecto.html'
    context_object_name = 'obj'
    success_url = reverse_lazy('graficos')
    success_message = "Proyecto elimiando satisfactoriamente"


########################
## Vistas Modelo Pago ##
########################
@login_required(login_url='login')
def detalle_pago(request, id):
    pagos = Pago.objects.filter(proyecto_id=id)
    total_pagos = Pago.objects.filter(proyecto_id=id).aggregate(Total_Pagos=Sum('valor_pago'))
    if total_pagos['Total_Pagos'] == None:
       total_pagos['Total_Pagos'] = 0
    try:
        e = Pago.objects.get(id=id)
    except Pago.DoesNotExist:
        e = None
    if e == None:
        vp = Proyecto.objects.get(id=id)
        vpp = vp.valor_proyecto  - total_pagos['Total_Pagos']
    else:
        vp = Proyecto.objects.get(id=e.id)
        vpp = vp.valor_proyecto  - total_pagos['Total_Pagos']
    return render(request, 'proyectos/pago/pago_detalle.html', {'pagos':pagos,'total_pagos':total_pagos,'vp':vp,'vpp':vpp})


@login_required(login_url='login')
@permission_required('proyectos.change_pago', login_url='sin_privilegios')
def editar_pago(request,id):
    pago = get_object_or_404(Pago, pk=id)
    proyecto_id = pago.proyecto.id
    if request.method == 'POST':
        form_pago = PagoForm(request.POST, instance=pago)
        if form_pago.is_valid():
            pago.um = request.user.id
            form_pago.save()
            messages.success(request, 'Pago editado correctamente')
            return redirect('detalle_proyecto', id=proyecto_id)
    else:
        form_pago = PagoForm(instance=pago)
        return render(request, 'proyectos/pago/editar_pago.html', {'form_pago':form_pago})


class BorrarPago(SuccessMessageMixin,SinPrivilegios, DeleteView):
    permission_required = "proyectos.delete_pago"
    model = Pago
    template_name = 'proyectos/pago/borrar_pago.html'
    context_object_name = 'obj'
    success_url = reverse_lazy('graficos')
    success_message = "Pago eliminado correctamente"


#########################
## Datos Para Gráficos ##
#########################
@login_required(login_url='login')
def graficos(request):
    labels = []
    data = []

    proyecto_macro = ProyectoMacro.objects.all()
    queryset = Proyecto.objects.filter(proyecto_macro_id=None)
    imagenes = Imagen.objects.all()[:6]

    cant_proy_bun = Proyecto.objects.filter(terminal="BUN", proyecto_macro_id=None).count()
    cant_proy_bun_eje = Proyecto.objects.filter(terminal="BUN", estado="EJ", proyecto_macro_id=None).count()
    cant_proy_bun_sus = Proyecto.objects.filter(terminal="BUN", estado="S", proyecto_macro_id=None).count()
    cant_proy_bun_canc = Proyecto.objects.filter(terminal="BUN", estado="C", proyecto_macro_id=None).count()
    cant_proy_bun_fin = Proyecto.objects.filter(terminal="BUN", estado="F", proyecto_macro_id=None).count()
    cant_proy_bun_macro = ProyectoMacro.objects.filter(terminal="BUN").count()
    cant_proy_bun_eje_macro = ProyectoMacro.objects.filter(terminal="BUN", estado="EJ").count()
    cant_proy_bun_sus_macro = ProyectoMacro.objects.filter(terminal="BUN", estado="S").count()
    cant_proy_bun_canc_macro = ProyectoMacro.objects.filter(terminal="BUN", estado="C").count()
    cant_proy_bun_fin_macro = ProyectoMacro.objects.filter(terminal="BUN", estado="F").count()

    cant_proy_ctg = Proyecto.objects.filter(terminal="CTG", proyecto_macro_id=None).count()
    cant_proy_ctg_eje = Proyecto.objects.filter(terminal="CTG", estado="EJ", proyecto_macro_id=None).count()
    cant_proy_ctg_sus = Proyecto.objects.filter(terminal="CTG", estado="S", proyecto_macro_id=None).count()
    cant_proy_ctg_canc = Proyecto.objects.filter(terminal="CTG", estado="C", proyecto_macro_id=None).count()
    cant_proy_ctg_fin = Proyecto.objects.filter(terminal="CTG", estado="F", proyecto_macro_id=None).count()
    cant_proy_ctg_macro = ProyectoMacro.objects.filter(terminal="CTG").count()
    cant_proy_ctg_eje_macro = ProyectoMacro.objects.filter(terminal="CTG", estado="EJ").count()
    cant_proy_ctg_sus_macro = ProyectoMacro.objects.filter(terminal="CTG", estado="S").count()
    cant_proy_ctg_canc_macro = ProyectoMacro.objects.filter(terminal="CTG", estado="C").count()
    cant_proy_ctg_fin = ProyectoMacro.objects.filter(terminal="CTG", estado="F").count()

    cant_proy_bog = Proyecto.objects.filter(terminal="BOG", proyecto_macro_id=None).count()
    cant_proy_bog_eje = Proyecto.objects.filter(terminal="BOG", estado="EJ", proyecto_macro_id=None).count()
    cant_proy_bog_sus = Proyecto.objects.filter(terminal="BOG", estado="S", proyecto_macro_id=None).count()
    cant_proy_bog_canc = Proyecto.objects.filter(terminal="BOG", estado="C", proyecto_macro_id=None).count()
    cant_proy_bog_fin = Proyecto.objects.filter(terminal="BOG", estado="F", proyecto_macro_id=None).count()

    cant_proy_glb = Proyecto.objects.filter(terminal="GLB", proyecto_macro_id=None).count()
    cant_proy_glb_eje = Proyecto.objects.filter(terminal="GLB", estado="EJ", proyecto_macro_id=None).count()
    cant_proy_glb_sus = Proyecto.objects.filter(terminal="GLB", estado="S", proyecto_macro_id=None).count()
    cant_proy_glb_canc = Proyecto.objects.filter(terminal="GLB", estado="C", proyecto_macro_id=None).count()
    cant_proy_glb_fin = Proyecto.objects.filter(terminal="GLB", estado="F", proyecto_macro_id=None).count()

    suma_cantidad_proyectos = cant_proy_bun + cant_proy_ctg + cant_proy_bog + cant_proy_glb + cant_proy_bun_macro + cant_proy_ctg_macro
    suma_cant_proy_eje = cant_proy_bun_eje + cant_proy_ctg_eje + cant_proy_bog_eje + cant_proy_glb_eje + cant_proy_bun_eje_macro +cant_proy_ctg_eje_macro
    suma_cant_proy_sus = cant_proy_bun_sus + cant_proy_ctg_sus + cant_proy_bog_sus + cant_proy_glb_sus + cant_proy_bun_sus_macro + cant_proy_ctg_sus_macro
    suma_cant_proy_canc = cant_proy_bun_canc + cant_proy_ctg_canc + cant_proy_bog_canc + cant_proy_glb_canc + cant_proy_bun_canc_macro + cant_proy_ctg_canc_macro
    suma_cant_proy_fin = cant_proy_ctg_fin + cant_proy_bun_fin + cant_proy_bog_fin + cant_proy_glb_fin + cant_proy_bun_fin_macro
    
    total_proyecto = []
    total_proyecto.append(cant_proy_bun)
    total_proyecto.append(cant_proy_ctg)
    total_proyecto.append(cant_proy_bog)
    total_proyecto.append(cant_proy_glb)
    total_costo_proyectos = Proyecto.objects.all().aggregate(total_costo_proyectos=Sum('valor_proyecto'))
    total_pagos_proyectos = Pago.objects.all().aggregate(Total_Pagos_proyectos=Sum('valor_pago'))

    for p in queryset:
        labels.append(p.nombre)
        data.append(p.valor_proyecto)
        for d in proyecto_macro:
            labels.append(d.nombre)
            data.append(d.valor_proyecto)
    

    return render(request, 'proyectos/graficas/bar_chart.html', {
        'labels':labels, 
        'data':data, 
        'total_proyecto':total_proyecto, 
        'queryset':queryset,
        'total_costo_proyectos':total_costo_proyectos,
        'total_pagos_proyectos':total_pagos_proyectos,
        'suma_cantidad_proyectos':suma_cantidad_proyectos,
        'suma_cant_proy_eje':suma_cant_proy_eje,
        'suma_cant_proy_sus':suma_cant_proy_sus,
        'suma_cant_proy_fin':suma_cant_proy_fin,
        'suma_cant_proy_canc':suma_cant_proy_canc,
        'proyecto_macro':proyecto_macro,
        'imagenes':imagenes,
        })


#############################
## Vistas Modelo Documento ##
#############################
@login_required(login_url='login')
def detalle_documentos(request, id):
    documentos = Documento.objects.filter(proyecto_id=id)
    try:
        e = Documento.objects.get(id=id)
    except Documento.DoesNotExist:
        e = None
    if e == None:
        vp = Proyecto.objects.get(id=id)
    else:
        vp = Proyecto.objects.get(id=e.id)
    return render(request, 'proyectos/documento/documento_detalle.html',{'documentos':documentos, 'vp':vp})


class EditarDocumento(SuccessMessageMixin,SinPrivilegios, UpdateView):
    permission_required = "proyectos.change_documento"
    model = Documento
    template_name = 'proyectos/documento/editar_documento.html'
    context_object_name = 'obj'
    form_class = DocumentoForm
    success_url = reverse_lazy('proyectos_list')
    success_message = "Documento editado correctamente"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)

    # def get_success_url(self):
    #     return reverse_lazy('detalle_proyecto', args=[self.curso.id])


def editar_documento(request, id):
    documento = get_object_or_404(Documento, pk=id)
    proyecto_id = documento.proyecto.id
    if request.method == 'POST':
        form_documento = DocumentoForm(request.POST, instance=documento)
        if form_documento.is_valid():
            documento.um = request.user.id
            form_documento.save()
            messages.success(request, 'Documento editado correctamente')
            return redirect('detalle_proyecto', id=proyecto_id)
    else:
        form_documento = DocumentoForm(instance=documento)
        return render(request, 'proyectos/documento/editar_documento.html', {'form_documento':form_documento})



class BorrarDocumento(SuccessMessageMixin,SinPrivilegios, DeleteView):
    permission_required = "proyectos.delete_documento"
    model = Documento
    template_name = 'proyectos/documento/borrar_documento.html'
    context_object_name = 'obj'
    success_url = reverse_lazy('proyectos_list')
    success_message = "Documento borrado correctamente"


##########################
## Vistas Modelo Imágen ##
##########################
@login_required(login_url='login')
def detalle_imagen(request, id):
    imagenes = Imagen.objects.filter(proyecto_id=id)
    try:
        e = Imagen.objects.get(id=id)
    except Imagen.DoesNotExist:
        e = None
    if e == None:
        vp = Proyecto.objects.get(id=id)
    else:
        vp = Proyecto.objects.get(id=e.id)
    return render(request, 'proyectos/imagen/imagen_detalle.html',{'imagenes':imagenes,'vp':vp})


class BorrarImagen(SuccessMessageMixin,SinPrivilegios, DeleteView):
    permission_required = "proyectos.delete_imagen"
    model = Imagen
    template_name = 'proyectos/imagen/borrar_imagen.html'
    context_object_name = 'obj'
    success_url = reverse_lazy('proyectos_list')
    success_message = "Imágen cargada correctamente"


##########################
## Vistas Modelo Cambio ##
##########################
@login_required(login_url='login')
@permission_required('proyectos.change_cambio', login_url='sin_privilegios')
def editar_cambio(request, id):
    cambio = get_object_or_404(Cambio, pk=id)
    costo_actual = cambio.costo
    duracion_actual = cambio.duracion
    id_proyecto = cambio.proyecto.id
    if request.method == "POST":
        form = CambioForm(request.POST, instance=cambio)
        if form.is_valid():
            cd = form.cleaned_data
            costo = cd['costo']
            duracion = cd['duracion']
            proyecto = Proyecto.objects.filter(id=id_proyecto).values()
            dias = proyecto[0]['fecha_fin'] - proyecto[0]['fecha_inicio']

            if costo == None:
                valor_proyecto = proyecto[0]['valor_proyecto']

            if costo == None or costo_actual == None:
                costo = 0
                costo_actual = 0

            if costo > costo_actual:
                operacion_costo = costo - costo_actual
                valor_proyecto = operacion_costo + proyecto[0]['valor_proyecto']

            if costo < costo_actual:
                operacion_costo = costo_actual - costo
                valor_proyecto = proyecto[0]['valor_proyecto'] - operacion_costo

            if duracion == None:
                duracion_proy = int(dias.days)

            if duracion == None or duracion_actual == None:
                duracion = 0
                duracion_actual = 0

            if duracion > duracion_actual:
                operacion1 = (duracion - duracion_actual) + dias.days
                operacion =  operacion1 - dias.days
                duracion_proy = proyecto[0]['fecha_fin'] + datetime.timedelta(days=operacion)
            else:
                operacion1 =  dias.days -(duracion_actual - duracion)
                operacion = dias.days - operacion1
                duracion_proy = proyecto[0]['fecha_fin'] - datetime.timedelta(days=operacion)

            Proyecto.objects.filter(id=id_proyecto).update(valor_proyecto=valor_proyecto)
            Proyecto.objects.filter(id=id_proyecto).update(fecha_fin=duracion_proy)
            proyecto.um=request.user.id
            form.save()
            messages.success(request, 'Cambio editado correctamente')
            return redirect('detalle_proyecto', id=id_proyecto)

    else:
        form = CambioForm(instance=cambio)
        return render(request, 'proyectos/cambio/editar_cambio.html', {'form':form})


class BorrarCambio(SuccessMessageMixin,SinPrivilegios, DeleteView):
    permission_required = "proyectos.delete_cambio"
    model = Cambio
    template_name = 'proyectos/cambio/borrar_cambio.html'
    context_object_name = 'obj'
    success_url = reverse_lazy('proyectos_list')
    success_message = "Control de cambio borrado correctamente"


#######################
## Lisdatos Gráficas ##
#######################
@login_required(login_url='login')
def listado_proyectos_costo(request):
    total_proyectos = Proyecto.objects.filter().values()
    ProyectoMacro.objects.all().values()
    return render(request, 'proyectos/listas/listado_costo_proyectos.html', {'proyectos':total_proyectos})


@login_required(login_url='login')
def listado_pagos_proyectos(request):
    pagos = Pago.objects.all().order_by('-fecha_pago')
    return render(request, 'proyectos/listas/listado_pagos_proyectos.html', {'pagos':pagos})


@login_required(login_url='login')
def listado_proyectos_ejecucion(request):
    proy_eje = Proyecto.objects.filter(estado="EJ", proyecto_macro_id=None)
    proy_eje_macro = ProyectoMacro.objects.filter(estado="EJ")
    return render(request, 'proyectos/listas/listado_proyectos_eje.html', 
                {
                    'proy_eje':proy_eje, 
                    'proy_eje_macro':proy_eje_macro
                }
        )


@login_required(login_url='login')
def listado_proy_sus(request):
    proy_susp = Proyecto.objects.filter(estado="S")
    proy_susp_macro = ProyectoMacro.objects.filter(estado="S")
    return render(request, 'proyectos/listas/listado_proyectos_susp.html', 
                    {
                        'proy_susp':proy_susp,
                        'proy_susp_macro':proy_susp_macro
                    }
    )


@login_required(login_url='login')
def listado_proy_can(request):
    proy_canc = Proyecto.objects.filter(estado="C")
    proy_canc_macro = ProyectoMacro.objects.filter(estado="C")
    return render(request, 'proyectos/listas/listado_proyectos_canc.html', 
                    {
                        'proy_canc':proy_canc,
                        'proy_canc_macro':proy_canc_macro
                    })


@login_required(login_url='login')
def listado_proy_fin(request):
    proy_fin = Proyecto.objects.filter(estado="F")
    proy_fin_macro = ProyectoMacro.objects.filter(estado="F")
    return render(request, 'proyectos/listas/listado_proyectos_fin.html', 
                    {
                        'proy_fin':proy_fin,
                        'proy_fin_macro':proy_fin_macro
                    })


#############################
## Vistas Modelo Actividad ##
#############################
class CrearActividad(SuccessMessageMixin, SinPrivilegios, CreateView):
    permission_required = "proyectos.add_actividad"
    model = Actividad
    template_name = 'proyectos/actividad/crear_actividad.html'
    form_class = ActividadForm
    success_url = reverse_lazy('graficos')
    success_message = 'Actividad creada correctamente'

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)


@login_required(login_url='login')
def detalle_actividad(request, id):
    actividades = Actividad.objects.filter(proyecto_id=id)
    try:
        e = Actividad.objects.get(id=id)
    except Actividad.DoesNotExist:
        e = None
    if e == None:
        vp = Proyecto.objects.get(id=id)
    else:
        vp = Proyecto.objects.get(id=e.id)
    return render(request, 'proyectos/actividad/actividad_detalle.html', {'actividades': actividades, 'vp':vp})


@login_required(login_url='login')
@permission_required('proyectos.change_actividad', login_url='sin_privilegios')
def editar_actividad(request, id):
    actividad = get_object_or_404(Actividad, pk=id)
    id_proyecto = actividad.proyecto.id
    if request.method == 'POST':
        form_actividad = ActividadForm(request.POST, instance=actividad)
        if form_actividad.is_valid():
            actividad.um = request.user.id
            form_actividad.save()
            messages.success(request, 'Actividad editada correctamente')
            return redirect('detalle_proyecto', id=id_proyecto)
    else:
        form_actividad = ActividadForm(instance=actividad)
        return render(request, 'proyectos/actividad/actualizar_actividad.html', {'form_actividad':form_actividad})



class BorrarActividad(SuccessMessageMixin, SinPrivilegios, DeleteView):
    permission_required = "proyectos.delete_actividad"
    model = Actividad
    context_object_name = 'obj'
    template_name = 'proyectos/actividad/borrar_actividad.html'
    success_url = reverse_lazy('graficos')
    success_message = 'Actividad borrada correctamente'



######################################
## Vistas Modelo BibliotecaProyecto ##
######################################

class CrearBiblioteca(SuccessMessageMixin, SinPrivilegios, CreateView):
    permission_required = 'proyectos.add_bibliotecaproyecto'
    model = BibliotecaProyecto
    template_name = 'proyectos/biblioteca/crear_bibliotecaProy.html'
    form_class = BibliotecaPryectoForm
    success_url = reverse_lazy('listado_biblioteca')
    success_message = 'Proyecto para biblioteca creado correctamente'

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)


class ListadoBiblioteca(SinPrivilegios, ListView):
    permission_required = 'proyectos.view_bibliotecaproyecto'
    model = BibliotecaProyecto
    template_name = 'proyectos/biblioteca/listado_bibliotecaProy.html'
    context_object_name = 'obj'


class DetalleBiblioteca(SinPrivilegios, DetailView):
    permission_required = "proyectos.view_bibliotecaproyecto"
    model = BibliotecaProyecto
    template_name = 'proyectos/biblioteca/detalle_bibliotecaProy.html'
    context_object_name = 'obj'


class EditarBiblioteca(SuccessMessageMixin, SinPrivilegios, UpdateView):
    permission_required = 'proyectos.change_bibliotecaproyecto'
    model = BibliotecaProyecto
    form_class = BibliotecaPryectoForm
    template_name = 'proyectos/biblioteca/editar_bibliotecaProy.html'
    success_url = reverse_lazy('listado_biblioteca')
    success_message = 'Proyecto para biblioteca editado correctamente'

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


class BorrarBiblioteca(SuccessMessageMixin, SinPrivilegios, DeleteView):
    permission_required = "proyectos.delete_bibliotecaproyecto"
    model = BibliotecaProyecto
    context_object_name = 'obj'
    template_name = 'proyectos/biblioteca/borrar_bibliotecaProy.html'
    success_url = reverse_lazy('listado_biblioteca')
    success_message = 'Proyecto para biblioteca borrado correctamente'


#################################
## Vistas Modelo ProyectoMacro ##
#################################

class CrearProyectoMacro(SuccessMessageMixin, SinPrivilegios, CreateView):
    permission_required = 'proyectos.add_proyectomacro'
    model = ProyectoMacro
    template_name = 'proyectos/macro/crear_proymacro.html'
    form_class = ProyectoMacroForm
    success_url = reverse_lazy('listado_proymacro')
    success_message = 'Proyecto Macro creado correctamente'

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)


class ListadoProyectosMacro(SinPrivilegios, ListView):
    permission_required = 'proyectos.view_proyectomacro'
    model = ProyectoMacro
    template_name = 'proyectos/macro/listado_proymacro.html'
    context_object_name = 'obj'


def detalle_proy_macro(request,id):
    proyecto_macro = get_object_or_404(ProyectoMacro, pk=id)
    proyectos_del_macro = Proyecto.objects.filter(proyecto_macro=id)
    valor_proyecto_macro = Proyecto.objects.filter(proyecto_macro=id).aggregate(Sum('valor_proyecto'))
    ProyectoMacro.objects.filter(pk=id).update(valor_proyecto=valor_proyecto_macro['valor_proyecto__sum'])

    return render(request, 'proyectos/macro/proyecto_macro_detalle.html', {
        'proyecto_macro':proyecto_macro,
        'proyectos_del_macro':proyectos_del_macro,
        'valor_proyecto_macro':valor_proyecto_macro,
         })


class EditarProyectoMacro(SuccessMessageMixin, SinPrivilegios, UpdateView):
    permission_required = 'proyectos.change_proyectomacro'
    model = ProyectoMacro
    template_name = 'proyectos/macro/editar_proymacro.html'
    form_class = ProyectoMacroForm
    success_url = reverse_lazy('listado_proymacro')
    success_message = 'Proyecto Macro editado correctamente'

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


class BorrarProyectoMacro(SuccessMessageMixin, SinPrivilegios, DeleteView):
    permission_required = "proyectos.delete_proyectomacro"
    model = ProyectoMacro
    context_object_name = 'obj'
    template_name = 'proyectos/macro/borrar_proymacro.html'
    success_url = reverse_lazy('listado_proymacro')
    success_message = 'Proyecto para biblioteca borrado correctamente'


def costos_del_macro(request, id):
    proyecto_macro = get_object_or_404(ProyectoMacro, pk=id)
    proyectos_del_macro = Proyecto.objects.filter(proyecto_macro=id).values()
    valor_proyecto_macro = Proyecto.objects.filter(proyecto_macro=id).aggregate(Sum('valor_proyecto'))

    idis = []
    for p in Proyecto.objects.filter(proyecto_macro=id).values():
        qs = p['id']
        idis.append(qs)

    suma_pagos = []
    for id in idis:
        qs = Pago.objects.filter(proyecto_id=id).values()
        for p in qs:
            qs_1 = p['valor_pago']
            suma_pagos.append(qs_1)

    total_pagos_macro = sum(suma_pagos)

    valor_por_pagar = valor_proyecto_macro['valor_proyecto__sum'] - total_pagos_macro

    return render(request, 'proyectos/macro/costos_proyecto_macro.html', {
        'valor_proyecto_macro':valor_proyecto_macro,
        'total_pagos_macro': total_pagos_macro,
        'valor_por_pagar':valor_por_pagar,
        'proyecto_macro':proyecto_macro
        })


###################################
## Vistas Modelo Actividad Macro ##
###################################
class CrearActividadMacro(SuccessMessageMixin, SinPrivilegios, CreateView):
    permission_required = "proyectos.add_actividad_macro"
    model = ActividadMacro
    template_name = 'proyectos/actividad/crear_actividad_macro.html'
    form_class = ActividadMacroForm
    success_url = reverse_lazy('graficos')
    success_message = 'Actividad creada correctamente'

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)


@login_required(login_url='login')
def detalle_actividad_macro(request, id):
    actividades = ActividadMacro.objects.filter(proyecto_id=id)
    try:
        e = ActividadMacro.objects.get(id=id)
    except ActividadMacro.DoesNotExist:
        e = None
    if e == None:
        vp = ProyectoMacro.objects.get(id=id)
    else:
        vp = ProyectoMacro.objects.get(id=e.id)
    return render(request, 'proyectos/actividad/actividad_detalle_macro.html', {'actividades': actividades, 'vp':vp})


class ActualizarActividadMacro(SuccessMessageMixin, SinPrivilegios, UpdateView):
    permission_required = "proyectos.change_actividad_macro"
    model = ActividadMacro
    form_class = ActividadMacroForm
    template_name = 'proyectos/actividad/actualizar_actividad_macro.html'
    success_url = reverse_lazy('graficos')
    success_message = 'Actividad actualizada correctamente'

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


class BorrarActividadMacro(SuccessMessageMixin, SinPrivilegios, DeleteView):
    permission_required = "proyectos.delete_actividad_macro"
    model = ActividadMacro
    context_object_name = 'obj'
    template_name = 'proyectos/actividad/borrar_actividad_macro.html'
    success_url = reverse_lazy('graficos')
    success_message = 'Actividad borrada correctamente'



###################################
## Vistas Modelo Documento Macro ##
###################################
class DocumentoCreateMacro(SuccessMessageMixin,SinPrivilegios, CreateView):
    permission_required = "proyectos.add_documento_macro"
    model = DocumentoMacro
    template_name = 'proyectos/documento/crear_documento_macro.html'
    form_class = DocumentoMacroForm
    success_url = reverse_lazy('graficos')
    success_message = "Documento cargado correctamente"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)


@login_required(login_url='login')
def detalle_documentos_macro(request, id):
    documentos = DocumentoMacro.objects.filter(proyecto_id=id)
    try:
        e = DocumentoMacro.objects.get(id=id)
    except DocumentoMacro.DoesNotExist:
        e = None
    if e == None:
        vp = ProyectoMacro.objects.get(id=id)
    else:
        vp = ProyectoMacro.objects.get(id=e.id)
    return render(request, 'proyectos/documento/documento_detalle_macro.html',{'documentos':documentos, 'vp':vp})


class EditarDocumentoMacro(SuccessMessageMixin,SinPrivilegios, UpdateView):
    permission_required = "proyectos.change_documento_macro"
    model = DocumentoMacro
    template_name = 'proyectos/documento/editar_documento_macro.html'
    context_object_name = 'obj'
    form_class = DocumentoMacroForm
    success_url = reverse_lazy('graficos')
    success_message = "Documento editado correctamente"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


class BorrarDocumentoMacro(SuccessMessageMixin,SinPrivilegios, DeleteView):
    permission_required = "proyectos.delete_documento_macro"
    model = DocumentoMacro
    template_name = 'proyectos/documento/borrar_documento_macro.html'
    context_object_name = 'obj'
    success_url = reverse_lazy('graficos')
    success_message = "Documento borrado correctamente"


###########################
## Vistas Modelo Curva S ##
###########################
@login_required(login_url='login')
@permission_required('proyectos.change_curva_s', login_url='sin_privilegios')
def editar_curva(request,id):
    curva = get_object_or_404(CurvaS, pk=id)
    proyecto_id = curva.proyecto.id
    if request.method == 'POST':
        form_curva = CurvaForm(request.POST, instance=curva)
        if form_curva.is_valid():
            curva.um = request.user.id
            form_curva.save()
            messages.success(request, 'curva editada correctamente')
            return redirect('detalle_proyecto', id=proyecto_id)
    else:
        form_curva = CurvaForm(instance=curva)
        return render(request, 'proyectos/curva/editar_curva.html', {'form_curva':form_curva})


@login_required(login_url='login')
@permission_required('proyectos.view_curva_s', login_url='sin_privilegios')
def lista_puntos(request, id):
    puntos = CurvaS.objects.filter(proyecto_id=id)
    return render(request, 'proyectos/curva/lista_puntos.html', {'puntos':puntos})


##########################
## Vistas Modelo Costos ##
##########################
class EditarCosto(SuccessMessageMixin , SinPrivilegios, UpdateView):
    permission_required = "proyectos.change_costo"
    model = Costo
    template_name = 'proyectos/costo/editar_costo.html'
    context_object_name = 'costo_editar'
    form_class = CostosForm
    success_url = reverse_lazy('graficos')
    success_message = "Costo editado correctamente"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)