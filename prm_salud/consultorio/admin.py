# admin.py para consultorio

from django.contrib import admin
from .models import (
    PerfilUsuario, Paciente, Profesional, Sesion, NotaSesion, PlanTerapeutico, Actividad,
    DocumentoPaciente, Cita, HistorialCambios, Consentimiento,
    PacientePotencial, InteraccionMarketing, RedSocial, BotWhatsappMensaje, CalendarioCumpleanos
)

class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'rol')
    search_fields = ('user__username', 'rol')
    list_filter = ('rol',)
    raw_id_fields = ('user',)
    fields = ('user', 'rol')

admin.site.register(PerfilUsuario, PerfilUsuarioAdmin)

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'cedula_identidad', 'direccion', 'fecha_nacimiento', 'edad_admin')
    search_fields = ('nombres', 'apellidos', 'cedula_identidad', 'direccion')

    def edad_admin(self, obj):
        return obj.edad()
    edad_admin.short_description = 'Edad'

admin.site.register(Profesional)
admin.site.register(Sesion)
admin.site.register(NotaSesion)
admin.site.register(PlanTerapeutico)
admin.site.register(Actividad)
admin.site.register(DocumentoPaciente)
admin.site.register(Cita)
admin.site.register(HistorialCambios)
admin.site.register(Consentimiento)

class MarketingAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        # Oculta este ModelAdmin del bloque Consultorio
        return {}

@admin.register(PacientePotencial)
class PacientePotencialAdmin(admin.ModelAdmin):
    list_display = ("nombres", "apellidos", "estado", "canal_origen", "fecha_contacto")
    search_fields = ("nombres", "apellidos", "email", "telefono")
    list_filter = ("estado", "canal_origen")
    def get_app_label(self, model):
        return 'Marketing'

@admin.register(InteraccionMarketing)
class InteraccionMarketingAdmin(admin.ModelAdmin):
    list_display = ("paciente_potencial", "tipo_interaccion", "fecha_interaccion")
    search_fields = ("paciente_potencial__nombres", "paciente_potencial__apellidos")
    list_filter = ("tipo_interaccion",)
    def get_app_label(self, model):
        return 'Marketing'

@admin.register(RedSocial)
class RedSocialAdmin(admin.ModelAdmin):
    list_display = ("canal", "fecha_registro", "seguidores", "interacciones", "comentarios")
    list_filter = ("canal",)
    def get_app_label(self, model):
        return 'Marketing'

@admin.register(BotWhatsappMensaje)
class BotWhatsappMensajeAdmin(admin.ModelAdmin):
    list_display = ("remitente", "destinatario", "fecha_envio", "es_respuesta")
    search_fields = ("remitente", "destinatario", "mensaje")
    list_filter = ("es_respuesta",)
    def get_app_label(self, model):
        return 'Marketing'

@admin.register(CalendarioCumpleanos)
class CalendarioCumpleanosAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo", "fecha_cumpleanos", "email")
    list_filter = ("tipo",)
    search_fields = ("nombre", "email")
    def get_app_label(self, model):
        return 'Marketing'
