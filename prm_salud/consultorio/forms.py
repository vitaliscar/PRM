from django import forms
from django.contrib.auth.models import User
from .models import PerfilUsuario, Paciente, Profesional, Sesion, NotaSesion, PlanTerapeutico, Actividad, DocumentoPaciente, Cita, HistorialCambios, Consentimiento, PacientePotencial, InteraccionMarketing, RedSocial, BotWhatsappMensaje, CalendarioCumpleanos

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']
        help_texts = {
            'username': '',
        }

class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['rol']

from django import forms
from .models import Paciente

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'
        widgets = {
            'fecha_nacimiento': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['foto'].widget.attrs.update({'accept': 'image/*'})
        if self.instance and self.instance.fecha_nacimiento:
            # Mostrar en formato regional DD/MM/YYYY
            self.initial['fecha_nacimiento'] = self.instance.fecha_nacimiento.strftime('%d/%m/%Y')

    def clean_fecha_nacimiento(self):
        # Convertir de DD/MM/YYYY a YYYY-MM-DD antes de guardar
        fecha = self.cleaned_data['fecha_nacimiento']
        return fecha.strftime('%Y-%m-%d')


class SesionForm(forms.ModelForm):
    class Meta:
        model = Sesion
        fields = '__all__'
        widgets = {
            'fecha_sesion': forms.DateInput(attrs={'type': 'date'}),
        }

class NotaSesionForm(forms.ModelForm):
    class Meta:
        model = NotaSesion
        fields = '__all__'
        widgets = {
            'fecha_nota': forms.DateInput(attrs={'type': 'date'}),
        }

class PlanTerapeuticoForm(forms.ModelForm):
    class Meta:
        model = PlanTerapeutico
        fields = '__all__'
        widgets = {
            'fecha_inicio_plan': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin_estimada': forms.DateInput(attrs={'type': 'date'}),
            'fecha_finalizacion_real': forms.DateInput(attrs={'type': 'date'}),
        }

class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = '__all__'
        widgets = {
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'}),
        }

class SolicitudUsuarioForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Contraseña"
    )
    cargo = forms.CharField(
        label="Cargo de trabajo",
        max_length=100,
        required=True,
        help_text="Este campo ayudará al administrador a asignarte un rol en la aplicación."
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'cargo', 'email', 'password']
        help_texts = {
            'username': '',
        }

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'aurora-input w-full'}),
            'first_name': forms.TextInput(attrs={'class': 'aurora-input w-full'}),
            'last_name': forms.TextInput(attrs={'class': 'aurora-input w-full'}),
            'email': forms.EmailInput(attrs={'class': 'aurora-input w-full'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'ml-2'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'ml-2'}),
        }

class PerfilForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['rol']
        widgets = {
            'rol': forms.Select(attrs={'class': 'aurora-input w-full'}),
        }

class DocumentoPacienteForm(forms.ModelForm):
    class Meta:
        model = DocumentoPaciente
        fields = '__all__'

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = '__all__'
        widgets = {
            'fecha': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class HistorialCambiosForm(forms.ModelForm):
    class Meta:
        model = HistorialCambios
        fields = '__all__'

class ConsentimientoForm(forms.ModelForm):
    class Meta:
        model = Consentimiento
        fields = '__all__'

class PacientePotencialForm(forms.ModelForm):
    class Meta:
        model = PacientePotencial
        fields = '__all__'
        widgets = {
            'fecha_contacto': forms.DateInput(attrs={'type': 'date'}),
            'fecha_conversion': forms.DateInput(attrs={'type': 'date'}),
        }

class InteraccionMarketingForm(forms.ModelForm):
    class Meta:
        model = InteraccionMarketing
        fields = '__all__'

class RedSocialForm(forms.ModelForm):
    class Meta:
        model = RedSocial
        fields = '__all__'
        widgets = {
            'fecha_registro': forms.DateInput(attrs={'type': 'date'}),
        }

class BotWhatsappMensajeForm(forms.ModelForm):
    class Meta:
        model = BotWhatsappMensaje
        fields = '__all__'

class CalendarioCumpleanosForm(forms.ModelForm):
    class Meta:
        model = CalendarioCumpleanos
        fields = '__all__'
        widgets = {
            'fecha_cumpleanos': forms.DateInput(attrs={'type': 'date'}),
        }
