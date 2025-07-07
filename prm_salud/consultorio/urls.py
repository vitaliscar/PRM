# consultorio/urls.py
from django.urls import path
from . import views
from .views import HistorialPacienteView, SolicitudUsuarioView

app_name = 'consultorio' # Define el namespace de la app para usar 'consultorio:paciente_list'

urlpatterns = [
    # Dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),

    # Pacientes
    path('pacientes/', views.PacienteListView.as_view(), name='paciente_list'),
    path('pacientes/nuevo/', views.PacienteCreateView.as_view(), name='paciente_create'),
    path('pacientes/<uuid:pk>/', HistorialPacienteView.as_view(), name='paciente_detail'), # 'pk' es el id_paciente (UUID)
    path('pacientes/<uuid:pk>/editar/', views.PacienteUpdateView.as_view(), name='paciente_update'),
    path('pacientes/<uuid:pk>/eliminar/', views.PacienteDeleteView.as_view(), name='paciente_delete'),

    # Profesionales
    path('profesionales/', views.ProfesionalListView.as_view(), name='profesional_list'),
    path('profesionales/nuevo/', views.ProfesionalCreateView.as_view(), name='profesional_create'),
    path('profesionales/<int:pk>/editar/', views.ProfesionalUpdateView.as_view(), name='profesional_update'),
    path('profesionales/<int:pk>/eliminar/', views.ProfesionalDeleteView.as_view(), name='profesional_delete'),

    # Sesiones
    path('sesiones/', views.SesionListView.as_view(), name='sesion_list'),
    path('sesiones/nueva/', views.SesionCreateView.as_view(), name='sesion_create'),
    path('sesiones/<int:pk>/editar/', views.SesionUpdateView.as_view(), name='sesion_update'),
    path('sesiones/<int:pk>/eliminar/', views.SesionDeleteView.as_view(), name='sesion_delete'),
    path('sesiones/<int:pk>/', views.SesionDetailView.as_view(), name='sesion_detail'),

    # Notas de Sesión (usamos sesion_id para asociar la nota)
    path('sesiones/<int:sesion_id>/nota/crear_o_editar/', views.NotaSesionCreateUpdateView.as_view(), name='nota_sesion_create_update'),
    path('notas/<int:pk>/editar/', views.NotaSesionUpdateView.as_view(), name='nota_update'),
    path('notas/<int:pk>/eliminar/', views.NotaSesionDeleteView.as_view(), name='nota_delete'),
    path('notas/', views.NotaSesionListView.as_view(), name='nota_list'),
    path('notas/<int:pk>/', views.NotaSesionDetailView.as_view(), name='nota_detail'),

    # Planes Terapéuticos
    path('planes/', views.PlanTerapeuticoListView.as_view(), name='plan_list'),
    path('planes/nuevo/', views.PlanTerapeuticoCreateView.as_view(), name='plan_create'),
    path('planes/<int:pk>/editar/', views.PlanTerapeuticoUpdateView.as_view(), name='plan_update'),
    path('planes/<int:pk>/eliminar/', views.PlanTerapeuticoDeleteView.as_view(), name='plan_delete'),
    path('planes/<int:pk>/', views.PlanTerapeuticoDetailView.as_view(), name='plan_detail'),

    # Actividades
    path('actividades/', views.ActividadListView.as_view(), name='actividad_list'),
    path('actividades/nueva/', views.ActividadCreateView.as_view(), name='actividad_create'),
    path('actividades/<int:pk>/editar/', views.ActividadUpdateView.as_view(), name='actividad_update'),
    path('actividades/<int:pk>/eliminar/', views.ActividadDeleteView.as_view(), name='actividad_delete'),

    # Gestión de usuarios
    path('usuarios/', views.UserListView.as_view(), name='user_list'),
    path('usuarios/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('usuarios/<int:pk>/editar/', views.UserUpdateView.as_view(), name='user_update'),
    path('usuarios/<int:pk>/eliminar/', views.UserDeleteView.as_view(), name='user_delete'),

    # Solicitud de Usuario
    path('solicitud-usuario/', SolicitudUsuarioView.as_view(), name='solicitud_usuario'),

    # Documentos de Paciente
    path('documentos/', views.DocumentoPacienteListView.as_view(), name='documentopaciente_list'),
    path('documentos/nuevo/', views.DocumentoPacienteCreateView.as_view(), name='documentopaciente_create'),
    path('documentos/<int:pk>/', views.DocumentoPacienteDetailView.as_view(), name='documentopaciente_detail'),
    path('documentos/<int:pk>/editar/', views.DocumentoPacienteUpdateView.as_view(), name='documentopaciente_update'),
    path('documentos/<int:pk>/eliminar/', views.DocumentoPacienteDeleteView.as_view(), name='documentopaciente_delete'),

    # Citas
    path('citas/', views.CitaListView.as_view(), name='cita_list'),
    path('citas/nueva/', views.CitaCreateView.as_view(), name='cita_create'),
    path('citas/<int:pk>/', views.CitaDetailView.as_view(), name='cita_detail'),
    path('citas/<int:pk>/editar/', views.CitaUpdateView.as_view(), name='cita_update'),
    path('citas/<int:pk>/eliminar/', views.CitaDeleteView.as_view(), name='cita_delete'),

    # Historial de Cambios
    path('historiales/', views.HistorialCambiosListView.as_view(), name='historialcambios_list'),
    path('historiales/nuevo/', views.HistorialCambiosCreateView.as_view(), name='historialcambios_create'),
    path('historiales/<int:pk>/', views.HistorialCambiosDetailView.as_view(), name='historialcambios_detail'),
    path('historiales/<int:pk>/editar/', views.HistorialCambiosUpdateView.as_view(), name='historialcambios_update'),
    path('historiales/<int:pk>/eliminar/', views.HistorialCambiosDeleteView.as_view(), name='historialcambios_delete'),

    # Consentimientos
    path('consentimientos/', views.ConsentimientoListView.as_view(), name='consentimiento_list'),
    path('consentimientos/nuevo/', views.ConsentimientoCreateView.as_view(), name='consentimiento_create'),
    path('consentimientos/<int:pk>/', views.ConsentimientoDetailView.as_view(), name='consentimiento_detail'),
    path('consentimientos/<int:pk>/editar/', views.ConsentimientoUpdateView.as_view(), name='consentimiento_update'),
    path('consentimientos/<int:pk>/eliminar/', views.ConsentimientoDeleteView.as_view(), name='consentimiento_delete'),

    # --- Marketing y Trazabilidad ---
    # Pacientes Potenciales
    path('marketing/potenciales/', views.PacientePotencialListView.as_view(), name='pacientepotencial_list'),
    path('marketing/potenciales/nuevo/', views.PacientePotencialCreateView.as_view(), name='pacientepotencial_create'),
    path('marketing/potenciales/<uuid:pk>/', views.PacientePotencialDetailView.as_view(), name='pacientepotencial_detail'),
    path('marketing/potenciales/<uuid:pk>/editar/', views.PacientePotencialUpdateView.as_view(), name='pacientepotencial_update'),
    path('marketing/potenciales/<uuid:pk>/eliminar/', views.PacientePotencialDeleteView.as_view(), name='pacientepotencial_delete'),

    # Interacciones de Marketing
    path('marketing/interacciones/', views.InteraccionMarketingListView.as_view(), name='interaccionmarketing_list'),
    path('marketing/interacciones/nueva/', views.InteraccionMarketingCreateView.as_view(), name='interaccionmarketing_create'),
    path('marketing/interacciones/<int:pk>/', views.InteraccionMarketingDetailView.as_view(), name='interaccionmarketing_detail'),
    path('marketing/interacciones/<int:pk>/editar/', views.InteraccionMarketingUpdateView.as_view(), name='interaccionmarketing_update'),
    path('marketing/interacciones/<int:pk>/eliminar/', views.InteraccionMarketingDeleteView.as_view(), name='interaccionmarketing_delete'),

    # Red Social
    path('marketing/redes/', views.RedSocialListView.as_view(), name='redsocial_list'),
    path('marketing/redes/nueva/', views.RedSocialCreateView.as_view(), name='redsocial_create'),
    path('marketing/redes/<int:pk>/', views.RedSocialDetailView.as_view(), name='redsocial_detail'),
    path('marketing/redes/<int:pk>/editar/', views.RedSocialUpdateView.as_view(), name='redsocial_update'),
    path('marketing/redes/<int:pk>/eliminar/', views.RedSocialDeleteView.as_view(), name='redsocial_delete'),

    # Bot WhatsApp
    path('marketing/botwhatsapp/', views.BotWhatsappMensajeListView.as_view(), name='botwhatsappmensaje_list'),
    path('marketing/botwhatsapp/nuevo/', views.BotWhatsappMensajeCreateView.as_view(), name='botwhatsappmensaje_create'),
    path('marketing/botwhatsapp/<int:pk>/', views.BotWhatsappMensajeDetailView.as_view(), name='botwhatsappmensaje_detail'),
    path('marketing/botwhatsapp/<int:pk>/editar/', views.BotWhatsappMensajeUpdateView.as_view(), name='botwhatsappmensaje_update'),
    path('marketing/botwhatsapp/<int:pk>/eliminar/', views.BotWhatsappMensajeDeleteView.as_view(), name='botwhatsappmensaje_delete'),

    # Cumpleaños
    path('marketing/cumpleanos/', views.CalendarioCumpleanosListView.as_view(), name='calendariocumpleanos_list'),
    path('marketing/cumpleanos/nuevo/', views.CalendarioCumpleanosCreateView.as_view(), name='calendariocumpleanos_create'),
    path('marketing/cumpleanos/<int:pk>/', views.CalendarioCumpleanosDetailView.as_view(), name='calendariocumpleanos_detail'),
    path('marketing/cumpleanos/<int:pk>/editar/', views.CalendarioCumpleanosUpdateView.as_view(), name='calendariocumpleanos_update'),
    path('marketing/cumpleanos/<int:pk>/eliminar/', views.CalendarioCumpleanosDeleteView.as_view(), name='calendariocumpleanos_delete'),
]
