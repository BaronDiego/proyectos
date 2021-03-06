from django.urls import path
from . import views

urlpatterns = [
    path('listado_proyectos/', views.ListaProyectos.as_view(), name='proyectos_list'),
    path('detalle/<int:id>/', views.detalle_proyecto, name='detalle_proyecto'),
    path('crear_proyecto/', views.CrearProyecto.as_view(), name='crear_proeycto'),
    path('editar/<pk>/', views.EditarProyecto.as_view(), name='editar_proyecto'),
    path('borrar_proyecto/<pk>/', views.BorrarProyecto.as_view(), name='borrar_proyecto'),
    # path('pago/', views.CrearPago.as_view(), name='crear_pago'),
    # path('pago/<pk>/', views.DetallePago.as_view(), name='detalle_apgo'),
    path('pago_detalle/<int:id>/', views.detalle_pago, name='detalle_pago'),
    path('editar_pago/<int:id>/', views.editar_pago, name='editar_pago'),
    path('borrar_pago/<pk>', views.BorrarPago.as_view(), name='borrar_pago'),
    # path('', views.graficos, name='graficos'),
    # path('documento/', views.DocumentoCreate.as_view(), name='crear_documento'),
    path('documento_detalle/<int:id>/', views.detalle_documentos, name='detalle_doc'),
    path('editar_documento/<int:id>/', views.editar_documento, name='editar_documento'),
    path('borrar_documento/<pk>/', views.BorrarDocumento.as_view(), name='borrar_documento'),
    # path('imagen/', views.CrearImagen.as_view(), name='cargar_imagen'),
    path('imagen_detalle/<int:id>/', views.detalle_imagen, name='detalle_imagen'),
    path('borrar_imagen/<pk>/', views.BorrarImagen.as_view(), name='borrar_imagen'),
    # path('crear_cambio/', views.crear_cambio, name='crear_cambio'),
    # path('detalle_cambio/<int:id>/', views.detalle_cambio, name='detalle_cambio'),
    path('editar_cambio/<int:id>/', views.editar_cambio, name='editar_cambio'),
    path('borrar_cambio/<pk>/', views.BorrarCambio.as_view(), name='borrar_cambio'),
    path('listado_costos_proyectos/', views.listado_proyectos_costo, name='listado_costos'),
    path('listado_pagos_proyectos/', views.listado_pagos_proyectos, name='listado_pagos'),
    path('listado_proy_ejec/', views.listado_proyectos_ejecucion, name='listado_proy_ejec'),
    path('listado_proy_susp/', views.listado_proy_sus, name='listado_proy_susp'),
    path('listado_proy_canc/', views.listado_proy_can, name='listado_proy_canc'),
    path('listado_proy_fin/', views.listado_proy_fin, name='listado_proy_fin'),
    path('crear_actividad/', views.CrearActividad.as_view(), name='crear_actividad'),
    path('detalle_actividad/<int:id>/', views.detalle_actividad, name='detalle_actividad'),
    path('actualizar_actividad/<int:id>/', views.editar_actividad, name='actualizar_actividad'),
    path('eliminar_actividad/<pk>/', views.BorrarActividad.as_view(), name='borrar_actividad'),
    path('listado_bibliotecaProyectos/', views.ListadoBiblioteca.as_view(), name='listado_biblioteca'),
    path('crear_bibliotecaProyectos/', views.CrearBiblioteca.as_view(), name='crear_biblioteca'),
    path('detalle_bibliotecaProyecto/<pk>', views.DetalleBiblioteca.as_view(), name='detalle_biblioteca'),
    path('editar_bibliotecaProyecto/<pk>', views.EditarBiblioteca.as_view(), name='editar_biblioteca'),
    path('borrar_bibliotecaProyecto/<pk>', views.BorrarBiblioteca.as_view(), name='borrar_biblioteca'),
    path('crear_proymacro/', views.CrearProyectoMacro.as_view(), name='crear_proymacro'),
    path('listado_proyectos_macro/', views.ListadoProyectosMacro.as_view(), name='listado_proymacro'),
    path('detalle_proyecto_macro/<int:id>/', views.detalle_proy_macro, name='detalle_proymacro'),
    path('editar_proyecto_macro/<pk>/', views.EditarProyectoMacro.as_view(), name='editar_proymacro'),
    path('borrar_proyecto_macro/<pk>/', views.BorrarProyectoMacro.as_view(), name='borrar_proymacro'),
    path('costos_detalle_macro/<int:id>/', views.costos_del_macro, name='detalle_costos_macro'),
    path('crear_actividad_macro/', views.CrearActividadMacro.as_view(), name='crear_actividad_macro'),
    path('detalle_actividad_macro/<int:id>/', views.detalle_actividad_macro, name='detalle_actividad_macro'),
    path('actualizar_actividad_macro/<pk>/', views.ActualizarActividadMacro.as_view(), name='actualizar_actividad_macro'),
    path('eliminar_actividad_macro/<pk>/', views.BorrarActividadMacro.as_view(), name='borrar_actividad_macro'),
    path('documento_macro/', views.DocumentoCreateMacro.as_view(), name='crear_documento_macro'),
    path('documento_detalle_macro/<int:id>/', views.detalle_documentos_macro, name='detalle_doc_macro'),
    path('editar_documento_macro/<pk>/', views.EditarDocumentoMacro.as_view(), name='editar_documento_macro'),
    path('borrar_documento_macro/<pk>/', views.BorrarDocumentoMacro.as_view(), name='borrar_documento_macro'),
    path('puntos_curva/<int:id>/', views.lista_puntos, name="puntos"),
    path('editar_punto/<int:id>/', views.editar_curva, name="editar_curva"),
    path('editar_costo/<pk>/', views.EditarCosto.as_view(), name="editar_costo"),
]