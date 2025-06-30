# consultorio/views.py
import datetime
import requests
import json # Para manejar datos JSON, especialmente para gráficos

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import ModelForm, DateInput, TimeInput, Textarea, Select, TextInput, NumberInput # Importa NumberInput para campos numéricos
from django.db import models  # <-- Agrega esta línea para importar models
from django.contrib.auth.models import User

# --- Importa Modelos ---
from .models import Paciente, Profesional, Sesion, NotaSesion, PlanTerapeutico, Actividad, PerfilUsuario
from .forms import UsuarioForm, PerfilForm, DocumentoPacienteForm, CitaForm, HistorialCambiosForm, ConsentimientoForm
from .models import PacientePotencial, InteraccionMarketing, RedSocial, BotWhatsappMensaje, CalendarioCumpleanos
from .forms import PacientePotencialForm, InteraccionMarketingForm, RedSocialForm, BotWhatsappMensajeForm, CalendarioCumpleanosForm

# --- Configuración de la API de Gemini (desde settings.py) ---
from django.conf import settings # Accede a las variables de settings.py

# =========================================================
# Mixins para Control de Roles y Permisos (Usan PerfilUsuario)
# =========================================================

class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Solo permite el acceso a administradores."""
    def test_func(self):
        return hasattr(self.request.user, 'perfilusuario') and self.request.user.perfilusuario.is_admin()

class PsicologoRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Solo permite el acceso a psicólogos."""
    def test_func(self):
        return hasattr(self.request.user, 'perfilusuario') and self.request.user.perfilusuario.is_psicologo()

class AdminOrPsicologoRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Permite el acceso a administradores o psicólogos."""
    def test_func(self):
        if hasattr(self.request.user, 'perfilusuario'):
            return self.request.user.perfilusuario.is_admin() or self.request.user.perfilusuario.is_psicologo()
        return False

class AllStaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Permite el acceso a cualquier miembro del personal (admin, psicólogo, asistente)."""
    def test_func(self):
        return hasattr(self.request.user, 'perfilusuario')

# =========================================================
# Formularios (usando Django ModelForms)
# =========================================================

# NOTA: Para todos los ModelForms, hemos añadido atributos 'class'
# a los widgets para facilitar la estilización con Tailwind CSS.
# Esto se repite para cada campo.

class PacienteForm(ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'
        exclude = ['id_paciente', 'fecha_registro'] # id_paciente se genera automáticamente, fecha_registro auto_now_add
        widgets = {
            'nombres': TextInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'apellidos': TextInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'fecha_nacimiento': DateInput(attrs={'type': 'date', 'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'genero': Select(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'cedula_identidad': TextInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'telefono': TextInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'email': TextInput(attrs={'type': 'email', 'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'estado_paciente': Select(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'fuente_referencia': Select(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'motivo_principal_consulta_inicial': Textarea(attrs={'rows': 3, 'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'estado_inicial_valoracion': TextInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
        }

class ProfesionalForm(ModelForm):
    class Meta:
        model = Profesional
        fields = '__all__'
        widgets = {
            'nombre_completo': TextInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'numero_colegiado': TextInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'especialidad_principal': Select(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'email_profesional': TextInput(attrs={'type': 'email', 'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'horario_atencion': TextInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
        }

class SesionForm(ModelForm):
    class Meta:
        model = Sesion
        fields = '__all__'
        exclude = ['duracion_minutos'] # Se calcula automáticamente
        widgets = {
            'paciente': Select(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'profesional': Select(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'fecha_sesion': DateInput(attrs={'type': 'date', 'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'hora_inicio': TimeInput(attrs={'type': 'time', 'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'hora_fin': TimeInput(attrs={'type': 'time', 'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'tipo_sesion': Select(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'estado_sesion': Select(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'motivo_cancelacion': Textarea(attrs={'rows': 3, 'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
        }

class NotaSesionForm(ModelForm):
    class Meta:
        model = NotaSesion
        fields = '__all__'
        widgets = {
            'subjetivo': Textarea(attrs={'rows': 4, 'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'objetivo': Textarea(attrs={'rows': 4, 'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'analisis': Textarea(attrs={'rows': 4, 'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'plan': Textarea(attrs={'rows': 4, 'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'diagnostico_dsm': TextInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'progreso_subjetivo_paciente': Select(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'progreso_objetivo_profesional': Select(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'tareas_asignadas': Textarea(attrs={'rows': 3, 'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'temas_abordados': TextInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
        }

class PlanTerapeuticoForm(ModelForm):
    class Meta:
        model = PlanTerapeutico
        fields = '__all__'
        widgets = {
            'paciente': Select(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'profesional': Select(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'nombre_plan': TextInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'fecha_inicio_plan': DateInput(attrs={'type': 'date', 'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'fecha_fin_estimada': DateInput(attrs={'type': 'date', 'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'objetivo_principal_terapeutico': Textarea(attrs={'rows': 3, 'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'metas_especificas': Textarea(attrs={'rows': 5, 'placeholder': 'Una meta por línea', 'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'enfoque_terapeutico': Select(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'estado_plan': Select(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'fecha_finalizacion_real': DateInput(attrs={'type': 'date', 'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'observaciones_plan': Textarea(attrs={'rows': 3, 'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
        }

class ActividadForm(ModelForm):
    class Meta:
        model = Actividad
        fields = '__all__'
        exclude = ['fecha_creacion'] # Se auto-genera
        widgets = {
            'paciente': Select(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'profesional_creador': Select(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'tipo_actividad': Select(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'descripcion': Textarea(attrs={'rows': 3, 'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'fecha_vencimiento': DateInput(attrs={'type': 'date', 'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'estado_actividad': Select(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500'}),
        }


# =========================================================
# Vistas para cada entidad
# =========================================================

# --- DASHBOARD ---
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'consultorio/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # --- Indicadores Clave ---
        context['total_pacientes'] = Paciente.objects.count()
        context['sesiones_realizadas'] = Sesion.objects.filter(estado_sesion='Realizada').count()
        context['notas_registradas'] = NotaSesion.objects.count()
        context['planes_activos'] = PlanTerapeutico.objects.filter(estado_plan='Activo').count()
        context['actividades_pendientes'] = Actividad.objects.filter(estado_actividad='Pendiente').count()
        context['total_profesionales'] = Profesional.objects.count()
        # --- Marketing ---
        today = datetime.date.today()
        context['leads_este_mes'] = PacientePotencial.objects.filter(fecha_contacto__month=today.month).count()
        context['leads_convertidos'] = PacientePotencial.objects.filter(fecha_contacto__month=today.month, estado='Convertido').count()
        context['seguidores_instagram'] = RedSocial.objects.filter(canal='Instagram').first().seguidores if RedSocial.objects.filter(canal='Instagram').exists() else 0
        context['interacciones_totales'] = InteraccionMarketing.objects.filter(fecha_interaccion__month=today.month).count()
        marketing_data = [
            {"name": "Instagram", "value": PacientePotencial.objects.filter(canal_origen='Instagram').count()},
            {"name": "Facebook", "value": PacientePotencial.objects.filter(canal_origen='Facebook').count()},
            {"name": "Web", "value": PacientePotencial.objects.filter(canal_origen='Web').count()},
            {"name": "Otro", "value": PacientePotencial.objects.exclude(canal_origen__in=['Instagram','Facebook','Web']).count()},
        ]
        context['marketing_data'] = json.dumps(marketing_data)

        # --- Datos para Gráficos (procesados en Python, pasados como JSON a JS en el template) ---
        # 1. Pacientes por Rango de Edad
        pacientes_por_edad_raw = {}
        today = datetime.date.today()
        for p in Paciente.objects.all():
            age = today.year - p.fecha_nacimiento.year - ((today.month, today.day) < (p.fecha_nacimiento.month, p.fecha_nacimiento.day))
            if age < 18: range_key = '0-17 años'
            elif 18 <= age <= 25: range_key = '18-25 años'
            elif 26 <= age <= 40: range_key = '26-40 años'
            elif 41 <= age <= 60: range_key = '41-60 años'
            elif age > 60: range_key = 'Más de 60 años'
            else: range_key = 'Desconocido'
            pacientes_por_edad_raw[range_key] = pacientes_por_edad_raw.get(range_key, 0) + 1
        
        # Ordenar los rangos de edad para la visualización
        age_order = ['0-17 años', '18-25 años', '26-40 años', '41-60 años', 'Más de 60 años', 'Desconocido']
        pacientes_por_edad_data = [{'name': r, 'value': pacientes_por_edad_raw.get(r, 0)} for r in age_order]
        context['pacientes_por_edad_data'] = json.dumps(pacientes_por_edad_data)

        # 2. Sesiones por Tipo
        sesiones_por_tipo_raw = {}
        for s in Sesion.objects.all():
            sesiones_por_tipo_raw[s.get_tipo_sesion_display()] = sesiones_por_tipo_raw.get(s.get_tipo_sesion_display(), 0) + 1
        sesiones_por_tipo_data = [{'name': k, 'value': v} for k, v in sesiones_por_tipo_raw.items()]
        context['sesiones_por_tipo_data'] = json.dumps(sesiones_por_tipo_data)

        # 3. Estado de Pacientes
        estado_pacientes_raw = {}
        for p in Paciente.objects.all():
            estado_pacientes_raw[p.get_estado_paciente_display()] = estado_pacientes_raw.get(p.get_estado_paciente_display(), 0) + 1
        estado_pacientes_data = [{'name': k, 'value': v} for k, v in estado_pacientes_raw.items()]
        context['estado_pacientes_data'] = json.dumps(estado_pacientes_data)
        
        # 4. Pacientes por Fuente de Referencia
        fuente_referencia_raw = {}
        for p in Paciente.objects.all():
            fuente_referencia_raw[p.get_fuente_referencia_display()] = fuente_referencia_raw.get(p.get_fuente_referencia_display(), 0) + 1
        fuente_referencia_data = [{'name': k, 'value': v} for k, v in fuente_referencia_raw.items()]
        context['fuente_referencia_data'] = json.dumps(fuente_referencia_data)

        # 5. Prevalencia de Diagnósticos (DSM-5) - Solo para Psicólogo/Admin
        if self.request.user.perfilusuario.is_psicologo() or self.request.user.perfilusuario.is_admin():
            diagnosticos_raw = {}
            for n in NotaSesion.objects.exclude(diagnostico_dsm__isnull=True).exclude(diagnostico_dsm__exact=''):
                diagnosticos_raw[n.diagnostico_dsm] = diagnosticos_raw.get(n.diagnostico_dsm, 0) + 1
            diagnosticos_data = [{'name': k, 'value': v} for k, v in diagnosticos_raw.items()]
            context['diagnosticos_data'] = json.dumps(diagnosticos_data)
        else:
            context['diagnosticos_data'] = json.dumps([]) # Vacío si no tiene permiso

        # Pasar el rol del usuario para controlar la visibilidad de gráficos y botones
        context['user_profile'] = self.request.user.perfilusuario
        context['es_psicologo'] = self.request.user.is_staff or self.request.user.groups.filter(name='psicologos').exists()
        return context

# --- PACIENTES ---
class PacienteListView(LoginRequiredMixin, ListView):
    model = Paciente
    template_name = 'consultorio/pacientes/paciente_list.html'
    context_object_name = 'pacientes'
    paginate_by = 10

    def get_queryset(self):
        # Permite buscar por nombre, apellido o cédula
        queryset = super().get_queryset()
        print(f"Initial queryset count: {queryset.count()}") # Debug print
        query = self.request.GET.get('q')
        print(f"Search query (q): {query}") # Debug print
        if query:
            queryset = queryset.filter(
                models.Q(nombres__icontains=query) |
                models.Q(apellidos__icontains=query) |
                models.Q(cedula_identidad__icontains=query)
            ).distinct()
            print(f"Filtered queryset count: {queryset.count()}") # Debug print
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(f"[DEBUG PacienteListView] Context pacientes: {context.get('pacientes')}")
        user = self.request.user
        perfil = getattr(user, 'perfilusuario', None)
        context['puede_crear'] = user.is_authenticated and perfil and (
            perfil.is_admin() or perfil.is_psicologo() or perfil.is_asistente()
        )
        context['puede_editar'] = context['puede_crear']
        context['puede_eliminar'] = user.is_authenticated and perfil and perfil.is_admin()
        context['user_profile'] = perfil
        context['es_psicologo'] = perfil.is_psicologo() if perfil else False
        return context

# Vista de detalle del paciente (ahora es el historial)
class HistorialPacienteView(LoginRequiredMixin, DetailView):
    model = Paciente
    template_name = 'consultorio/pacientes/paciente_detail.html'
    context_object_name = 'paciente'
    pk_url_kwarg = 'pk' # Asegura que use 'pk' de la URL para buscar el objeto (id_paciente)

    def get_object(self, queryset=None):
        return get_object_or_404(Paciente, id_paciente=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paciente = self.get_object()
        # Mostrar solo sesiones (no mezclar con notas)
        sesiones = Sesion.objects.filter(paciente=paciente).order_by('-fecha_sesion', '-hora_inicio')
        context['sesiones'] = sesiones
        context['user_profile'] = self.request.user.perfilusuario
        return context

# Vistas de creación/actualización/eliminación de Pacientes
class PacienteCreateView(AllStaffRequiredMixin, CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'consultorio/pacientes/paciente_form.html'
    success_url = reverse_lazy('consultorio:paciente_list')

    def get_success_url(self):
        return reverse_lazy('consultorio:paciente_list')

    def form_valid(self, form):
        from django.contrib import messages
        response = super().form_valid(form)
        messages.success(self.request, 'Paciente creado exitosamente.')
        return response

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.enctype = 'multipart/form-data'
        return form

class PacienteUpdateView(AllStaffRequiredMixin, UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'consultorio/pacientes/paciente_form.html'
    success_url = reverse_lazy('consultorio:paciente_list')
    pk_url_kwarg = 'pk' # Usa el id_paciente como PK en la URL

    def get_object(self, queryset=None):
        return get_object_or_404(Paciente, id_paciente=self.kwargs['pk'])

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.enctype = 'multipart/form-data'
        return form

class PacienteDeleteView(AdminRequiredMixin, DeleteView):
    model = Paciente
    template_name = 'consultorio/confirm_delete.html'
    success_url = reverse_lazy('consultorio:paciente_list')
    pk_url_kwarg = 'pk' # Usa el id_paciente como PK en la URL

    def get_object(self, queryset=None):
        return get_object_or_404(Paciente, id_paciente=self.kwargs['pk'])


# --- SESIONES ---
class SesionListView(LoginRequiredMixin, ListView):
    model = Sesion
    template_name = 'consultorio/sesiones/sesion_list.html'
    context_object_name = 'sesiones'
    ordering = ['-fecha_sesion', '-hora_inicio']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        perfil = getattr(user, 'perfilusuario', None)
        context['puede_crear'] = user.is_authenticated and perfil and (
            perfil.is_admin() or perfil.is_psicologo() or perfil.is_asistente()
        )
        context['puede_editar'] = context['puede_crear']
        context['puede_notas'] = user.is_authenticated and perfil and (
            perfil.is_admin() or perfil.is_psicologo()
        )
        context['puede_eliminar'] = user.is_authenticated and perfil and perfil.is_admin()
        context['user_profile'] = perfil
        return context

class SesionCreateView(AllStaffRequiredMixin, CreateView):
    model = Sesion
    form_class = SesionForm
    template_name = 'consultorio/sesiones/sesion_form.html'
    success_url = reverse_lazy('consultorio:sesion_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pacientes'] = Paciente.objects.all()
        context['profesionales'] = Profesional.objects.all()
        return context

class SesionUpdateView(AllStaffRequiredMixin, UpdateView):
    model = Sesion
    form_class = SesionForm
    template_name = 'consultorio/sesiones/sesion_form.html'
    success_url = reverse_lazy('consultorio:sesion_list')
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pacientes'] = Paciente.objects.all()
        context['profesionales'] = Profesional.objects.all()
        return context

class SesionDeleteView(AdminRequiredMixin, DeleteView):
    model = Sesion
    template_name = 'consultorio/confirm_delete.html'
    success_url = reverse_lazy('consultorio:sesion_list')
    pk_url_kwarg = 'pk'


# --- NOTAS DE SESIÓN ---
class NotaSesionCreateUpdateView(AdminOrPsicologoRequiredMixin, CreateView, UpdateView):
    # Usa una sola vista para crear y actualizar notas.
    model = NotaSesion
    form_class = NotaSesionForm
    template_name = 'consultorio/notas/nota_form.html'
    success_url = reverse_lazy('consultorio:sesion_list') # Redirige a la lista de sesiones

    def get_object(self, queryset=None):
        # Intenta obtener la nota si ya existe para la sesión dada (sesion_id de la URL)
        sesion_id = self.kwargs.get('sesion_id')
        if sesion_id:
            try:
                # Si es un Update, busca la nota por el ID de sesión
                return NotaSesion.objects.get(sesion__id=sesion_id)
            except NotaSesion.DoesNotExist:
                # Si no existe, es una Creación, devuelve None
                return None
        # Si no hay sesion_id en la URL (ej. si se accede por pk de nota), usa el PK estándar
        return super().get_object(queryset)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        sesion_id = self.kwargs.get('sesion_id')
        if sesion_id:
            sesion = get_object_or_404(Sesion, pk=sesion_id)
            kwargs['initial'] = {
                'sesion': sesion, # Asignar la sesión al formulario
                'paciente': sesion.paciente,
                'profesional': sesion.profesional,
            }
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sesion_id = self.kwargs.get('sesion_id')
        if sesion_id:
            context['sesion'] = get_object_or_404(Sesion, pk=sesion_id)
        # Pasar el resumen generado si existe en el objeto (para display)
        if self.object and self.object.generated_summary:
            context['generated_summary'] = self.object.generated_summary
        # Permiso para mostrar botón de resumen IA
        user = self.request.user
        context['es_psicologo'] = user.is_staff or user.groups.filter(name='psicologos').exists()
        return context

    def form_valid(self, form):
        # Antes de guardar, asigna las FKs que no están en el formulario directamente
        sesion_id = self.kwargs.get('sesion_id')
        if sesion_id:
            sesion = get_object_or_404(Sesion, pk=sesion_id)
            form.instance.sesion = sesion
            form.instance.paciente = sesion.paciente
            form.instance.profesional = sesion.profesional

        # Lógica para llamar a la API de Gemini si se pulsó el botón
        if 'generar_resumen' in self.request.POST:
            subjetivo = form.cleaned_data.get('subjetivo', '')
            objetivo = form.cleaned_data.get('objetivo', '')
            analisis = form.cleaned_data.get('analisis', '')
            plan = form.cleaned_data.get('plan', '')

            prompt = f"""Dadas las siguientes notas de sesión de psicología con el formato S.O.A.P. (Subjetivo, Objetivo, Análisis, Plan), por favor proporciona un resumen conciso resaltando los temas principales, los hallazgos clave y los puntos de acción relevantes.
            
            Notas S: {subjetivo}
            O: {objetivo}
            A: {analisis}
            P: {plan}
            
            Resumen:"""

            # Llama a la API de Gemini (clave desde settings.py)
            GEMINI_API_KEY = settings.GEMINI_API_KEY
            API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

            headers = {
                "Content-Type": "application/json"
            }
            payload = {
                "contents": [{"role": "user", "parts": [{"text": prompt}]}]
            }

            try:
                response = requests.post(f"{API_URL}?key={GEMINI_API_KEY}", headers=headers, json=payload)
                response.raise_for_status() # Lanza un error para códigos de estado HTTP incorrectos
                result = response.json()
                if result.get('candidates') and len(result['candidates']) > 0 and \
                   result['candidates'][0].get('content') and \
                   result['candidates'][0]['content'].get('parts') and \
                   len(result['candidates'][0]['content']['parts']) > 0:
                    generated_text = result['candidates'][0]['content']['parts'][0]['text']
                    form.instance.generated_summary = generated_text
                else:
                    form.instance.generated_summary = "Error: No se pudo obtener respuesta de la IA. Formato inesperado."
                    print(f"Gemini API response structure unexpected: {result}")
            except requests.exceptions.RequestException as e:
                form.instance.generated_summary = f"Error al conectar con la IA: {e}. Por favor, verifica tu clave API o la conexión a internet."
                print(f"Error calling Gemini API: {e}")
            
            # Si se generó el resumen y no se está guardando, renderizar de nuevo con el resumen
            # Si el usuario solo hizo clic en "generar_resumen", no queremos guardar la nota todavía
            if 'guardar' not in self.request.POST: # Asume que el botón "Guardar" tiene name="guardar"
                # Forzar un re-render del formulario con el resumen generado
                form.instance.pk = self.object.pk if self.object else None # Para que el formulario sepa si es update
                return self.render_to_response(self.get_context_data(form=form))

        # Si no se pulsó el botón de generar resumen o si se pulsó guardar, procede con el guardado normal
        return super().form_valid(form)

class NotaSesionUpdateView(UpdateView):
    model = NotaSesion
    fields = ['subjetivo', 'objetivo', 'analisis', 'plan']
    template_name = 'consultorio/notas/nota_form.html'
    context_object_name = 'nota'
    success_url = '/consultorio/sesiones/'

class NotaSesionDeleteView(DeleteView):
    model = NotaSesion
    template_name = 'consultorio/confirm_delete.html'
    context_object_name = 'nota'
    success_url = '/consultorio/sesiones/'

class NotaSesionListView(ListView):
    model = NotaSesion
    template_name = 'consultorio/notas/nota_list.html'
    context_object_name = 'notas'


# --- PROFESIONALES ---
class ProfesionalListView(LoginRequiredMixin, ListView):
    model = Profesional
    template_name = 'consultorio/profesionales/profesional_list.html'
    context_object_name = 'profesionales'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        en_grupo_psico = user.groups.filter(name='psicologos').exists()
        en_grupo_asist = user.groups.filter(name='asistentes').exists()
        context['puede_crear'] = user.is_authenticated and (user.is_staff or en_grupo_psico or en_grupo_asist)
        context['puede_editar'] = context['puede_crear']
        context['puede_eliminar'] = user.is_authenticated and user.is_staff
        context['user_profile'] = getattr(user, 'perfilusuario', None)
        return context

class ProfesionalCreateView(LoginRequiredMixin, CreateView):
    model = Profesional
    form_class = ProfesionalForm
    template_name = 'consultorio/profesionales/profesional_form.html'
    success_url = reverse_lazy('consultorio:profesional_list')

class ProfesionalUpdateView(LoginRequiredMixin, UpdateView):
    model = Profesional
    form_class = ProfesionalForm
    template_name = 'consultorio/profesionales/profesional_form.html'
    success_url = reverse_lazy('consultorio:profesional_list')
    pk_url_kwarg = 'pk'

class ProfesionalDeleteView(LoginRequiredMixin, DeleteView):
    model = Profesional
    template_name = 'consultorio/confirm_delete.html'
    success_url = reverse_lazy('consultorio:profesional_list')
    pk_url_kwarg = 'pk'


# --- PLANES TERAPÉUTICOS ---
class PlanTerapeuticoListView(LoginRequiredMixin, ListView):
    model = PlanTerapeutico
    template_name = 'consultorio/planes/plan_list.html'
    context_object_name = 'planes'

    def get_queryset(self):
        queryset = super().get_queryset()
        print(f"Total de planes terapéuticos: {queryset.count()}")
        for plan in queryset:
            print(f"  - ID: {plan.id}, Nombre: {plan.nombre_plan}")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        perfil = getattr(user, 'perfilusuario', None)
        # Solo admin o psicólogo pueden crear/editar/eliminar
        puede_editar = False
        if perfil:
            puede_editar = perfil.is_admin() or perfil.is_psicologo()
        context['puede_crear'] = puede_editar
        context['puede_editar'] = puede_editar
        context['puede_eliminar'] = perfil.is_admin() if perfil else False
        context['pacientes'] = Paciente.objects.all()
        context['profesionales'] = Profesional.objects.all()
        context['user_profile'] = perfil
        return context

class PlanTerapeuticoCreateView(AdminOrPsicologoRequiredMixin, CreateView):
    model = PlanTerapeutico
    form_class = PlanTerapeuticoForm
    template_name = 'consultorio/planes/plan_form.html'
    success_url = reverse_lazy('consultorio:plan_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pacientes'] = Paciente.objects.all()
        context['profesionales'] = Profesional.objects.all()
        return context
    
    def form_valid(self, form):
        # Manejar el campo JSONField de metas_especificas
        metas_raw = form.cleaned_data.get('metas_especificas')
        if metas_raw:
            # Convierte el texto de la textarea a una lista de strings
            form.instance.metas_especificas = [m.strip() for m in metas_raw.split('\n') if m.strip()]
        else:
            form.instance.metas_especificas = [] # Asegura que sea una lista vacía si está vacío

        return super().form_valid(form)


class PlanTerapeuticoUpdateView(AdminOrPsicologoRequiredMixin, UpdateView):
    model = PlanTerapeutico
    form_class = PlanTerapeuticoForm
    template_name = 'consultorio/planes/plan_form.html'
    success_url = reverse_lazy('consultorio:plan_list')
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pacientes'] = Paciente.objects.all()
        context['profesionales'] = Profesional.objects.all()
        # Para que la textarea muestre las metas como texto multilinea
        if self.object.metas_especificas and isinstance(self.object.metas_especificas, list):
            context['form'].fields['metas_especificas'].initial = "\n".join(self.object.metas_especificas)
        return context
    
    def form_valid(self, form):
        # Manejar el campo JSONField de metas_especificas
        metas_raw = form.cleaned_data.get('metas_especificas')
        if metas_raw:
            form.instance.metas_especificas = [m.strip() for m in metas_raw.split('\n') if m.strip()]
        else:
            form.instance.metas_especificas = []

        return super().form_valid(form)

class PlanTerapeuticoDeleteView(AdminRequiredMixin, DeleteView):
    model = PlanTerapeutico
    template_name = 'consultorio/confirm_delete.html'
    success_url = reverse_lazy('consultorio:plan_list')
    pk_url_kwarg = 'pk'


# --- ACTIVIDADES ---
class ActividadListView(LoginRequiredMixin, ListView):
    model = Actividad
    template_name = 'consultorio/actividades/actividad_list.html'
    context_object_name = 'actividades'
    ordering = ['estado_actividad', 'fecha_vencimiento']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        en_grupo_psico = user.groups.filter(name='psicologos').exists()
        en_grupo_asist = user.groups.filter(name='asistentes').exists()
        context['puede_crear'] = user.is_authenticated and (user.is_staff or en_grupo_psico or en_grupo_asist)
        context['puede_editar'] = context['puede_crear']
        context['puede_eliminar'] = user.is_authenticated and user.is_staff
        context['pacientes'] = Paciente.objects.all()
        context['profesionales'] = Profesional.objects.all()
        context['user_profile'] = getattr(user, 'perfilusuario', None)
        return context


class ActividadCreateView(LoginRequiredMixin, CreateView): # No se requiere rol específico por ahora
    model = Actividad
    form_class = ActividadForm
    template_name = 'consultorio/actividades/actividad_form.html'
    success_url = reverse_lazy('consultorio:actividad_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pacientes'] = Paciente.objects.all()
        context['profesionales'] = Profesional.objects.all()
        return context

class ActividadUpdateView(LoginRequiredMixin, UpdateView):
    model = Actividad
    form_class = ActividadForm
    template_name = 'consultorio/actividades/actividad_form.html'
    success_url = reverse_lazy('consultorio:actividad_list')
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pacientes'] = Paciente.objects.all()
        context['profesionales'] = Profesional.objects.all()
        return context

class ActividadDeleteView(AdminRequiredMixin, DeleteView):
    model = Actividad
    template_name = 'consultorio/confirm_delete.html'
    success_url = reverse_lazy('consultorio:actividad_list')
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Necesario para mostrar nombres en la lista
        context['pacientes'] = Paciente.objects.all() 
        context['profesionales'] = Profesional.objects.all()
        return context

# --- DOCUMENTOS DEL PACIENTE ---
from .models import DocumentoPaciente

class DocumentoPacienteListView(LoginRequiredMixin, ListView):
    model = DocumentoPaciente
    template_name = 'consultorio/documentos/documentopaciente_list.html'
    context_object_name = 'documentos'

class DocumentoPacienteDetailView(LoginRequiredMixin, DetailView):
    model = DocumentoPaciente
    template_name = 'consultorio/documentos/documentopaciente_detail.html'
    context_object_name = 'documento'

class DocumentoPacienteCreateView(LoginRequiredMixin, CreateView):
    model = DocumentoPaciente
    form_class = DocumentoPacienteForm
    template_name = 'consultorio/documentos/documentopaciente_form.html'
    success_url = reverse_lazy('consultorio:documentopaciente_list')

class DocumentoPacienteUpdateView(LoginRequiredMixin, UpdateView):
    model = DocumentoPaciente
    form_class = DocumentoPacienteForm
    template_name = 'consultorio/documentos/documentopaciente_form.html'
    success_url = reverse_lazy('consultorio:documentopaciente_list')

class DocumentoPacienteDeleteView(LoginRequiredMixin, DeleteView):
    model = DocumentoPaciente
    template_name = 'consultorio/documentos/documentopaciente_confirm_delete.html'
    success_url = reverse_lazy('consultorio:documentopaciente_list')


# --- CITAS ---
from .models import Cita

class CitaListView(LoginRequiredMixin, ListView):
    model = Cita
    template_name = 'consultorio/citas/cita_list.html'
    context_object_name = 'citas'

class CitaDetailView(LoginRequiredMixin, DetailView):
    model = Cita
    template_name = 'consultorio/citas/cita_detail.html'
    context_object_name = 'cita'

class CitaCreateView(LoginRequiredMixin, CreateView):
    model = Cita
    form_class = CitaForm
    template_name = 'consultorio/citas/cita_form.html'
    success_url = reverse_lazy('consultorio:cita_list')

class CitaUpdateView(LoginRequiredMixin, UpdateView):
    model = Cita
    form_class = CitaForm
    template_name = 'consultorio/citas/cita_form.html'
    success_url = reverse_lazy('consultorio:cita_list')

class CitaDeleteView(LoginRequiredMixin, DeleteView):
    model = Cita
    template_name = 'consultorio/citas/cita_confirm_delete.html'
    success_url = reverse_lazy('consultorio:cita_list')


# --- HISTORIAL DE CAMBIOS ---
from .models import HistorialCambios

class HistorialCambiosListView(LoginRequiredMixin, ListView):
    model = HistorialCambios
    template_name = 'consultorio/historiales/historialcambios_list.html'
    context_object_name = 'historiales'

class HistorialCambiosDetailView(LoginRequiredMixin, DetailView):
    model = HistorialCambios
    template_name = 'consultorio/historiales/historialcambios_detail.html'
    context_object_name = 'historial'

class HistorialCambiosCreateView(LoginRequiredMixin, CreateView):
    model = HistorialCambios
    form_class = HistorialCambiosForm
    template_name = 'consultorio/historiales/historialcambios_form.html'
    success_url = reverse_lazy('consultorio:historialcambios_list')

class HistorialCambiosUpdateView(LoginRequiredMixin, UpdateView):
    model = HistorialCambios
    form_class = HistorialCambiosForm
    template_name = 'consultorio/historiales/historialcambios_form.html'
    success_url = reverse_lazy('consultorio:historialcambios_list')

class HistorialCambiosDeleteView(LoginRequiredMixin, DeleteView):
    model = HistorialCambios
    template_name = 'consultorio/historiales/historialcambios_confirm_delete.html'
    success_url = reverse_lazy('consultorio:historialcambios_list')


# --- CONSENTIMIENTOS ---
from .models import Consentimiento

class ConsentimientoListView(LoginRequiredMixin, ListView):
    model = Consentimiento
    template_name = 'consultorio/consentimientos/consentimiento_list.html'
    context_object_name = 'consentimientos'

class ConsentimientoDetailView(LoginRequiredMixin, DetailView):
    model = Consentimiento
    template_name = 'consultorio/consentimientos/consentimiento_detail.html'
    context_object_name = 'consentimiento'

class ConsentimientoCreateView(LoginRequiredMixin, CreateView):
    model = Consentimiento
    form_class = ConsentimientoForm
    template_name = 'consultorio/consentimientos/consentimiento_form.html'
    success_url = reverse_lazy('consultorio:consentimiento_list')

class ConsentimientoUpdateView(LoginRequiredMixin, UpdateView):
    model = Consentimiento
    form_class = ConsentimientoForm
    template_name = 'consultorio/consentimientos/consentimiento_form.html'
    success_url = reverse_lazy('consultorio:consentimiento_list')

class ConsentimientoDeleteView(LoginRequiredMixin, DeleteView):
    model = Consentimiento
    template_name = 'consultorio/consentimientos/consentimiento_confirm_delete.html'
    success_url = reverse_lazy('consultorio:consentimiento_list')


# --- VISTAS DUPLICADAS: COMENTADAS PARA EVITAR CONFLICTOS ---
'''
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from .models import Paciente, Profesional, Sesion, NotaSesion, PlanTerapeutico, Actividad
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView
from .forms import UserEditForm, PerfilUsuarioForm, PacienteForm
from django.views import View
from django.shortcuts import get_object_or_404, render, redirect

class DashboardView(TemplateView):
    template_name = 'consultorio/dashboard.html'

# Pacientes
class PacienteListView(ListView):
    model = Paciente
    template_name = 'consultorio/pacientes/paciente_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['puede_crear'] = user.is_authenticated and (
            user.perfilusuario.is_admin() or user.perfilusuario.is_psicologo() or user.perfilusuario.is_asistente()
        )
        return context

class PacienteCreateView(CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'consultorio/pacientes/paciente_form.html'

class HistorialPacienteView(TemplateView):
    template_name = 'consultorio/pacientes/paciente_detail.html'

class PacienteUpdateView(UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'consultorio/pacientes/paciente_form.html'
'''

def get_menu_items(request):
    return [
        {'url': reverse('consultorio:dashboard'), 'icon': 'home', 'label': 'Inicio', 'active': request.path == '/consultorio/'},
        {'url': reverse('consultorio:paciente_list'), 'icon': 'users', 'label': 'Pacientes', 'active': 'pacientes' in request.path},
        {'url': reverse('consultorio:sesion_list'), 'icon': 'calendar', 'label': 'Sesiones', 'active': 'sesiones' in request.path},
        {'url': reverse('consultorio:plan_list'), 'icon': 'clipboard-list', 'label': 'Planes Terapéuticos', 'active': 'planes' in request.path},
        {'url': reverse('consultorio:actividad_list'), 'icon': 'activity', 'label': 'Actividades', 'active': 'actividades' in request.path},
        {'url': reverse('consultorio:profesional_list'), 'icon': 'award', 'label': 'Profesionales', 'active': 'profesionales' in request.path},
        {'url': reverse('consultorio:user_list'), 'icon': 'user-plus', 'label': 'Usuarios', 'active': 'usuarios' in request.path},
    ]

class UserListView(AdminRequiredMixin, ListView):
    model = User
    template_name = 'consultorio/usuarios/user_list.html'
    context_object_name = 'usuarios'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = getattr(self.request.user, 'perfilusuario', None)
        return context

class UserDetailView(AdminRequiredMixin, DetailView):
    model = User
    template_name = 'consultorio/usuarios/user_detail.html'
    context_object_name = 'user'

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'consultorio/usuarios/user_form.html'
    success_url = reverse_lazy('consultorio:user_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Solo admin puede editar cualquier usuario, los demás solo su propio perfil
        if self.request.user.perfilusuario.is_admin() or self.request.user == obj:
            return obj
        else:
            # Redirige a detalle si intenta editar otro usuario
            return redirect('consultorio:user_detail', pk=obj.pk)

    def get_form_class(self):
        if self.request.user.perfilusuario.is_admin():
            return UsuarioForm
        else:
            # Solo campos básicos para usuarios normales
            class BasicUserForm(UsuarioForm):
                class Meta(UsuarioForm.Meta):
                    fields = ['username', 'first_name', 'last_name', 'email']
            return BasicUserForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Solo admin puede editar el rol
        if self.request.user.perfilusuario.is_admin():
            perfil_usuario = PerfilUsuario.objects.get(user=self.object)
            if self.request.method == 'POST':
                context['perfil_form'] = PerfilForm(self.request.POST, instance=perfil_usuario)
            else:
                context['perfil_form'] = PerfilForm(instance=perfil_usuario)
        else:
            context['perfil_form'] = None
        context['user_form'] = context['form']
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        # Si es admin, guarda el rol
        if self.request.user.perfilusuario.is_admin() and 'perfil_form' in self.get_context_data():
            perfil_form = self.get_context_data()['perfil_form']
            if perfil_form.is_valid():
                perfil_form.save()
        return response

class UserDeleteView(AdminRequiredMixin, DeleteView):
    model = User
    template_name = 'consultorio/usuarios/user_confirm_delete.html'
    success_url = reverse_lazy('consultorio:user_list')


# --- SOLICITUD DE USUARIO ---
from .forms import SolicitudUsuarioForm
from django.urls import reverse_lazy
from django.contrib import messages

class SolicitudUsuarioView(CreateView):
    template_name = "consultorio/auth/solicitud_usuario.html"
    form_class = SolicitudUsuarioForm
    success_url = reverse_lazy('consultorio:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.is_active = False  # El admin debe activar el usuario
        user.save()
        messages.success(self.request, "Tu solicitud fue enviada. Un administrador la revisará.")
        return super().form_valid(form)

# --- DETALLE DE NOTA DE SESIÓN ---
class NotaSesionDetailView(DetailView):
    model = NotaSesion
    template_name = 'consultorio/notas/nota_detail.html'
    context_object_name = 'nota'


# PacientePotencial CRUD
class PacientePotencialListView(LoginRequiredMixin, ListView):
    model = PacientePotencial
    template_name = 'consultorio/marketing/pacientepotencial_list.html'
    context_object_name = 'potenciales'

class PacientePotencialDetailView(LoginRequiredMixin, DetailView):
    model = PacientePotencial
    template_name = 'consultorio/marketing/pacientepotencial_detail.html'
    context_object_name = 'potencial'

class PacientePotencialCreateView(LoginRequiredMixin, CreateView):
    model = PacientePotencial
    form_class = PacientePotencialForm
    template_name = 'consultorio/marketing/pacientepotencial_form.html'
    success_url = reverse_lazy('consultorio:pacientepotencial_list')

class PacientePotencialUpdateView(LoginRequiredMixin, UpdateView):
    model = PacientePotencial
    form_class = PacientePotencialForm
    template_name = 'consultorio/marketing/pacientepotencial_form.html'
    success_url = reverse_lazy('consultorio:pacientepotencial_list')

class PacientePotencialDeleteView(LoginRequiredMixin, DeleteView):
    model = PacientePotencial
    template_name = 'consultorio/marketing/pacientepotencial_confirm_delete.html'
    success_url = reverse_lazy('consultorio:pacientepotencial_list')

# InteraccionMarketing CRUD
class InteraccionMarketingListView(LoginRequiredMixin, ListView):
    model = InteraccionMarketing
    template_name = 'consultorio/marketing/interaccionmarketing_list.html'
    context_object_name = 'interacciones'

class InteraccionMarketingDetailView(LoginRequiredMixin, DetailView):
    model = InteraccionMarketing
    template_name = 'consultorio/marketing/interaccionmarketing_detail.html'
    context_object_name = 'interaccion'

class InteraccionMarketingCreateView(LoginRequiredMixin, CreateView):
    model = InteraccionMarketing
    form_class = InteraccionMarketingForm
    template_name = 'consultorio/marketing/interaccionmarketing_form.html'
    success_url = reverse_lazy('consultorio:interaccionmarketing_list')

class InteraccionMarketingUpdateView(LoginRequiredMixin, UpdateView):
    model = InteraccionMarketing
    form_class = InteraccionMarketingForm
    template_name = 'consultorio/marketing/interaccionmarketing_form.html'
    success_url = reverse_lazy('consultorio:interaccionmarketing_list')

class InteraccionMarketingDeleteView(LoginRequiredMixin, DeleteView):
    model = InteraccionMarketing
    template_name = 'consultorio/marketing/interaccionmarketing_confirm_delete.html'
    success_url = reverse_lazy('consultorio:interaccionmarketing_list')

# RedSocial CRUD
class RedSocialListView(LoginRequiredMixin, ListView):
    model = RedSocial
    template_name = 'consultorio/marketing/redsocial_list.html'
    context_object_name = 'redes'

class RedSocialDetailView(LoginRequiredMixin, DetailView):
    model = RedSocial
    template_name = 'consultorio/marketing/redsocial_detail.html'
    context_object_name = 'redsocial'

class RedSocialCreateView(LoginRequiredMixin, CreateView):
    model = RedSocial
    form_class = RedSocialForm
    template_name = 'consultorio/marketing/redsocial_form.html'
    success_url = reverse_lazy('consultorio:redsocial_list')

class RedSocialUpdateView(LoginRequiredMixin, UpdateView):
    model = RedSocial
    form_class = RedSocialForm
    template_name = 'consultorio/marketing/redsocial_form.html'
    success_url = reverse_lazy('consultorio:redsocial_list')

class RedSocialDeleteView(LoginRequiredMixin, DeleteView):
    model = RedSocial
    template_name = 'consultorio/marketing/redsocial_confirm_delete.html'
    success_url = reverse_lazy('consultorio:redsocial_list')

# BotWhatsappMensaje CRUD
class BotWhatsappMensajeListView(LoginRequiredMixin, ListView):
    model = BotWhatsappMensaje
    template_name = 'consultorio/marketing/botwhatsappmensaje_list.html'
    context_object_name = 'mensajes'

class BotWhatsappMensajeDetailView(LoginRequiredMixin, DetailView):
    model = BotWhatsappMensaje
    template_name = 'consultorio/marketing/botwhatsappmensaje_detail.html'
    context_object_name = 'mensaje'

class BotWhatsappMensajeCreateView(LoginRequiredMixin, CreateView):
    model = BotWhatsappMensaje
    form_class = BotWhatsappMensajeForm
    template_name = 'consultorio/marketing/botwhatsappmensaje_form.html'
    success_url = reverse_lazy('consultorio:botwhatsappmensaje_list')

class BotWhatsappMensajeUpdateView(LoginRequiredMixin, UpdateView):
    model = BotWhatsappMensaje
    form_class = BotWhatsappMensajeForm
    template_name = 'consultorio/marketing/botwhatsappmensaje_form.html'
    success_url = reverse_lazy('consultorio:botwhatsappmensaje_list')

class BotWhatsappMensajeDeleteView(LoginRequiredMixin, DeleteView):
    model = BotWhatsappMensaje
    template_name = 'consultorio/marketing/botwhatsappmensaje_confirm_delete.html'
    success_url = reverse_lazy('consultorio:botwhatsappmensaje_list')

# CalendarioCumpleanos CRUD
class CalendarioCumpleanosListView(LoginRequiredMixin, ListView):
    model = CalendarioCumpleanos
    template_name = 'consultorio/marketing/calendariocumpleanos_list.html'
    context_object_name = 'cumples'

class CalendarioCumpleanosDetailView(LoginRequiredMixin, DetailView):
    model = CalendarioCumpleanos
    template_name = 'consultorio/marketing/calendariocumpleanos_detail.html'
    context_object_name = 'cumple'

class CalendarioCumpleanosCreateView(LoginRequiredMixin, CreateView):
    model = CalendarioCumpleanos
    form_class = CalendarioCumpleanosForm
    template_name = 'consultorio/marketing/calendariocumpleanos_form.html'
    success_url = reverse_lazy('consultorio:calendariocumpleanos_list')

class CalendarioCumpleanosUpdateView(LoginRequiredMixin, UpdateView):
    model = CalendarioCumpleanos
    form_class = CalendarioCumpleanosForm
    template_name = 'consultorio/marketing/calendariocumpleanos_form.html'
    success_url = reverse_lazy('consultorio:calendariocumpleanos_list')

class CalendarioCumpleanosDeleteView(LoginRequiredMixin, DeleteView):
    model = CalendarioCumpleanos
    template_name = 'consultorio/marketing/calendariocumpleanos_confirm_delete.html'
    success_url = reverse_lazy('consultorio:calendariocumpleanos_list')

# --- DETALLE DE PLAN TERAPÉUTICO ---
class PlanTerapeuticoDetailView(LoginRequiredMixin, DetailView):
    model = PlanTerapeutico
    template_name = 'consultorio/planes/plan_detail.html'
    context_object_name = 'plan'

    def get_object(self, queryset=None):
        return get_object_or_404(PlanTerapeutico, id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plan = self.get_object()
        context['paciente'] = plan.paciente
        context['profesional'] = plan.professional
        return context
