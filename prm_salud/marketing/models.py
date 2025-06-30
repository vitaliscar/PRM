from django.db import models
import uuid
from datetime import date

class PacientePotencial(models.Model):
    ESTADOS = [
        ('prospecto', 'Prospecto'),
        ('convertido', 'Convertido'),
        ('descartado', 'Descartado'),
    ]

    id_potencial = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    fecha_contacto = models.DateField(auto_now_add=True)
    canal_origen = models.CharField(
        max_length=50,
        choices=[
            ('Instagram', 'Instagram'),
            ('YouTube', 'YouTube'),
            ('WhatsApp', 'WhatsApp'),
            ('Directo', 'Directo'),
            ('Otro', 'Otro'),
        ],
        default='Directo'
    )
    estado = models.CharField(max_length=20, choices=ESTADOS, default='prospecto')
    fecha_conversion = models.DateField(blank=True, null=True, verbose_name="Fecha de Conversión")
    paciente = models.OneToOneField(
        'consultorio.Paciente',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='potencial',
        verbose_name="Paciente Convertido"
    )

    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.get_estado_display()})"

    def marcar_como_convertido(self, paciente_obj):
        self.estado = 'convertido'
        self.paciente = paciente_obj
        self.fecha_conversion = date.today()
        self.save()

class RedSocial(models.Model):
    CANALES = [
        ('Instagram', 'Instagram'),
        ('YouTube', 'YouTube'),
        ('Facebook', 'Facebook'),
        ('Twitter', 'Twitter'),
        ('Otro', 'Otro'),
    ]
    canal = models.CharField(max_length=30, choices=CANALES)
    fecha_registro = models.DateField(auto_now_add=True)
    seguidores = models.PositiveIntegerField()
    interacciones = models.PositiveIntegerField(blank=True, null=True)
    comentarios = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = "Métrica de Red Social"
        verbose_name_plural = "Métricas de Redes Sociales"
        ordering = ['-fecha_registro']

    def __str__(self):
        return f"{self.canal} - {self.fecha_registro} - Seguidores: {self.seguidores}"

class BotWhatsappMensaje(models.Model):
    remitente = models.CharField(max_length=50)
    destinatario = models.CharField(max_length=50)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    es_respuesta = models.BooleanField(default=False)
    paciente_potencial = models.ForeignKey(PacientePotencial, on_delete=models.SET_NULL, blank=True, null=True, related_name='mensajes_bot')
    paciente = models.ForeignKey('consultorio.Paciente', on_delete=models.SET_NULL, blank=True, null=True, related_name='mensajes_bot')

    def __str__(self):
        return f"Mensaje {self.fecha_envio.strftime('%d/%m/%Y %H:%M')} de {self.remitente}"

class CalendarioCumpleanos(models.Model):
    TIPOS = [
        ('paciente', 'Paciente'),
        ('equipo', 'Equipo del Centro'),
    ]
    tipo = models.CharField(max_length=20, choices=TIPOS)
    nombre = models.CharField(max_length=150)
    fecha_cumpleanos = models.DateField()
    email = models.EmailField(blank=True, null=True)

    class Meta:
        verbose_name = "Cumpleaños"
        verbose_name_plural = "Cumpleaños"
        ordering = ['fecha_cumpleanos']

    def __str__(self):
        return f"{self.nombre} - {self.get_tipo_display()} - {self.fecha_cumpleanos.strftime('%d/%m')}",
