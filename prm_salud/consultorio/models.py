# consultorio/models.py
from django.db import models
from django.contrib.auth.models import User # Django ya incluye un modelo de usuario
import uuid # Para generar IDs únicos para Pacientes
from taggit.managers import TaggableManager

# --- Gestión de Roles Personalizados ---
# Se utiliza signals para crear automáticamente un PerfilUsuario cuando se crea un User
from django.db.models.signals import post_save
from django.dispatch import receiver

class PerfilUsuario(models.Model):
    """
    Extiende el modelo User de Django para añadir un campo de rol.
    Esto es crucial para la gestión de permisos en la aplicación.
    """
    ROLES = [
        ('admin', 'Administrador'),
        ('psicologo', 'Psicólogo'),
        ('asistente', 'Asistente'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    rol = models.CharField(max_length=20, choices=ROLES, default='asistente')

    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuarios"

    def __str__(self):
        return f"{self.user.username} ({self.get_rol_display()})"

    # Métodos de conveniencia para verificar roles en templates/vistas
    def is_admin(self):
        return self.rol == 'admin'

    def is_psicologo(self):
        return self.rol == 'psicologo'

    def is_asistente(self):
        return self.rol == 'asistente'

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Crea o actualiza automáticamente el PerfilUsuario cuando se crea/actualiza un User.
    """
    if created:
        PerfilUsuario.objects.create(user=instance)
    # Si el usuario ya existe, asegúrate de que el perfil exista y se guarde
    instance.perfilusuario.save()

# --- Entidades Principales del PRM ---

class Paciente(models.Model):
    """
    Representa a un paciente en el sistema.
    Campos para análisis de reportes y demográficos.
    """
    id_paciente = models.CharField(max_length=50, unique=True, editable=False, primary_key=True) # ID único generado
    nombres = models.CharField(max_length=100, verbose_name="Nombres")
    apellidos = models.CharField(max_length=100, verbose_name="Apellidos")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento")
    genero = models.CharField(
        max_length=20,
        choices=[
            ('Femenino', 'Femenino'),
            ('Masculino', 'Masculino'),
            ('Prefiero no decir', 'Prefiero no decir')
        ],
        verbose_name="Género"
    )
    cedula_identidad = models.CharField(max_length=20, unique=True, verbose_name="Cédula de Identidad")
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    direccion = models.CharField(max_length=255, blank=True, null=True, verbose_name="Dirección")
    estado_paciente = models.CharField(
        max_length=20,
        choices=[
            ('Activo', 'Activo'),
            ('En Pausa', 'En Pausa'),
            ('Dado de Alta', 'Dado de Alta'),
            ('No Acude', 'No Acude'),
            ('Nuevo', 'Nuevo')
        ],
        default='Activo',
        verbose_name="Estado del Paciente"
    )
    fecha_registro = models.DateField(auto_now_add=True, verbose_name="Fecha de Registro")
    fuente_referencia = models.CharField(
        max_length=50,
        choices=[
            ('Recomendación de Paciente', 'Recomendación de Paciente'),
            ('Redes Sociales', 'Redes Sociales'),
            ('Google Ads', 'Google Ads'),
            ('Otro Profesional de Salud', 'Otro Profesional de Salud'),
            ('Directo', 'Directo'),
            ('Desconocido', 'Desconocido')
        ],
        default='Desconocido',
        verbose_name="Fuente de Referencia"
    )
    motivo_principal_consulta_inicial = models.TextField(blank=True, null=True, verbose_name="Motivo Principal de Consulta Inicial")
    estado_inicial_valoracion = models.CharField(max_length=50, blank=True, null=True, verbose_name="Estado Inicial de Valoración")
    foto = models.ImageField(upload_to='pacientes/fotos/', blank=True, null=True, verbose_name="Foto")
    foto_offset_x = models.PositiveSmallIntegerField(default=50, verbose_name="Posición X de la Foto")
    foto_offset_y = models.PositiveSmallIntegerField(default=50, verbose_name="Posición Y de la Foto")

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ['apellidos', 'nombres'] # Ordenar por apellido y nombre por defecto

    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.cedula_identidad})"

    def save(self, *args, **kwargs):
        if not self.id_paciente:
            self.id_paciente = str(uuid.uuid4()) # Genera un UUID para el ID
        super().save(*args, **kwargs)

    def edad(self):
        from datetime import date
        today = date.today()
        return today.year - self.fecha_nacimiento.year - (
            (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )

class Profesional(models.Model):
    """
    Representa a un profesional de la salud (psicólogo, etc.).
    """
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='profesional')
    nombre_completo = models.CharField(max_length=200, verbose_name="Nombre Completo")
    numero_colegiado = models.CharField(max_length=50, unique=True, verbose_name="Número Colegiado")
    especialidad_principal = models.CharField(
        max_length=50,
        choices=[
            ('Psicólogo Clínico', 'Psicólogo Clínico'),
            ('Neuropsicólogo', 'Neuropsicólogo'),
            ('Psicólogo Infanto-Juvenil', 'Psicólogo Infanto-Juvenil'),
            ('Terapeuta de Pareja', 'Terapeuta de Pareja'),
            ('Psicólogo Organizacional', 'Psicólogo Organizacional')
        ],
        verbose_name="Especialidad Principal"
    )
    email_profesional = models.EmailField(unique=True, verbose_name="Email Profesional")
    horario_atencion = models.CharField(max_length=200, blank=True, null=True, verbose_name="Horario de Atención")

    class Meta:
        verbose_name = "Profesional"
        verbose_name_plural = "Profesionales"
        ordering = ['nombre_completo']

    def __str__(self):
        return self.nombre_completo

class Sesion(models.Model):
    """
    Representa una sesión de consulta con un paciente.
    """
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='sesiones', verbose_name="Paciente")
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE, related_name='sesiones_atendidas', verbose_name="Profesional")
    fecha_sesion = models.DateField(verbose_name="Fecha de Sesión")
    hora_inicio = models.TimeField(verbose_name="Hora de Inicio")
    hora_fin = models.TimeField(verbose_name="Hora de Fin")
    duracion_minutos = models.IntegerField(blank=True, null=True, verbose_name="Duración (minutos)") # Se calcula en el método save
    tipo_sesion = models.CharField(
        max_length=50,
        choices=[
            ('Primera Consulta', 'Primera Consulta'),
            ('Seguimiento Individual', 'Seguimiento Individual'),
            ('Terapia de Pareja', 'Terapia de Pareja'),
            ('Terapia Familiar', 'Terapia Familiar'),
            ('Online', 'Online'),
            ('Presencial', 'Presencial'),
            ('Evaluación', 'Evaluación')
        ],
        verbose_name="Tipo de Sesión"
    )
    estado_sesion = models.CharField(
        max_length=30,  # Aumentado para soportar el valor más largo
        choices=[
            ('Programada', 'Programada'),
            ('Confirmada', 'Confirmada'),
            ('Realizada', 'Realizada'),
            ('Cancelada_Profesional', 'Cancelada por Profesional'),
            ('Cancelada_Paciente', 'Cancelada por Paciente'),
            ('No_Asistida', 'No Asistida')
        ],
        default='Programada',
        verbose_name="Estado de Sesión"
    )
    motivo_cancelacion = models.TextField(blank=True, null=True, verbose_name="Motivo de Cancelación")

    class Meta:
        verbose_name = "Sesión"
        verbose_name_plural = "Sesiones"
        ordering = ['-fecha_sesion', '-hora_inicio'] # Ordenar por fecha y hora descendente

    def save(self, *args, **kwargs):
        # Calcular duracion_minutos al guardar
        if self.hora_inicio and self.hora_fin:
            from datetime import datetime
            start_dt = datetime.combine(self.fecha_sesion, self.hora_inicio)
            end_dt = datetime.combine(self.fecha_sesion, self.hora_fin)
            self.duracion_minutos = int((end_dt - start_dt).total_seconds() / 60)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Sesión de {self.paciente} con {self.profesional} el {self.fecha_sesion}"

class NotaSesion(models.Model):
    """
    Detalle de la sesión en formato S.O.A.P. y resumen de IA.
    """
    VALORACION_CHOICES = [(i, str(i)) for i in range(1, 11)] # Escala del 1 al 10

    sesion = models.OneToOneField(Sesion, on_delete=models.CASCADE, related_name='nota_sesion', verbose_name="Sesión")
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='notas_sesion', verbose_name="Paciente")
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE, related_name='notas_creadas', verbose_name="Profesional")
    fecha_nota = models.DateField(auto_now_add=True, verbose_name="Fecha de Nota")
    subjetivo = models.TextField(blank=True, verbose_name="Subjetivo (S)")
    objetivo = models.TextField(blank=True, verbose_name="Objetivo (O)")
    analisis = models.TextField(blank=True, verbose_name="Análisis (A)")
    plan = models.TextField(blank=True, verbose_name="Plan (P)")
    diagnostico_dsm = models.CharField(max_length=100, blank=True, null=True, verbose_name="Diagnóstico (DSM-5)")
    progreso_subjetivo_paciente = models.IntegerField(blank=True, null=True, choices=VALORACION_CHOICES, verbose_name="Progreso Subjetivo del Paciente (1-10)")
    progreso_objetivo_profesional = models.IntegerField(blank=True, null=True, choices=VALORACION_CHOICES, verbose_name="Progreso Objetivo del Profesional (1-10)")
    tareas_asignadas = models.TextField(blank=True, verbose_name="Tareas Asignadas")
    temas_abordados = models.CharField(max_length=255, blank=True, verbose_name="Temas Abordados (Separar por comas)")
    generated_summary = models.TextField(blank=True, null=True, verbose_name="Resumen Generado por IA")
    etiquetas = TaggableManager(blank=True) # Requiere migración y posible uso de django-taggit

    class Meta:
        verbose_name = "Nota de Sesión"
        verbose_name_plural = "Notas de Sesión"
        ordering = ['-fecha_nota']

    def __str__(self):
        return f"Nota de sesión para {self.paciente} en {self.fecha_nota}"

class PlanTerapeutico(models.Model):
    """
    Representa un plan de tratamiento a largo plazo para un paciente.
    """
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='planes_terapeuticos', verbose_name="Paciente")
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE, related_name='planes_gestionados', verbose_name="Profesional")
    nombre_plan = models.CharField(max_length=200, verbose_name="Nombre del Plan")
    fecha_inicio_plan = models.DateField(verbose_name="Fecha de Inicio")
    fecha_fin_estimada = models.DateField(blank=True, null=True, verbose_name="Fecha de Fin Estimada")
    objetivo_principal_terapeutico = models.TextField(verbose_name="Objetivo Principal Terapéutico")
    metas_específicas = models.JSONField(default=list, blank=True, null=True, verbose_name="Metas Específicas") # Almacena una lista de strings
    enfoque_terapeutico = models.CharField(
        max_length=50,
        choices=[
            ('Cognitivo-Conductual', 'Cognitivo-Conductual'),
            ('Terapia Sistémica', 'Terapia Sistémica'),
            ('Psicoanálisis', 'Psicoanálisis'),
            ('Humanista', 'Humanista'),
            ('Integrativo', 'Integrativo')
        ],
        default='Cognitivo-Conductual',
        verbose_name="Enfoque Terapéutico"
    )
    estado_plan = models.CharField(
        max_length=20,
        choices=[
            ('Activo', 'Activo'),
            ('Finalizado', 'Finalizado'),
            ('En Pausa', 'En Pausa'),
            ('Cancelado', 'Cancelado')
        ],
        default='Activo',
        verbose_name="Estado del Plan"
    )
    fecha_finalizacion_real = models.DateField(blank=True, null=True, verbose_name="Fecha de Finalización Real")
    observaciones_plan = models.TextField(blank=True, null=True, verbose_name="Observaciones del Plan")

    class Meta:
        verbose_name = "Plan Terapéutico"
        verbose_name_plural = "Planes Terapéuticos"
        ordering = ['-fecha_inicio_plan']

    def __str__(self):
        return f"Plan '{self.nombre_plan}' para {self.paciente}"

class Actividad(models.Model):
    """
    Representa una tarea o recordatorio asociado a un paciente o profesional.
    """
    paciente = models.ForeignKey(Paciente, on_delete=models.SET_NULL, null=True, blank=True, related_name='actividades', verbose_name="Paciente Asociado")
    profesional_creador = models.ForeignKey(Profesional, on_delete=models.SET_NULL, null=True, blank=True, related_name='actividades_creadas', verbose_name="Profesional Creador")
    tipo_actividad = models.CharField(
        max_length=50,
        choices=[
            ('Llamada de seguimiento', 'Llamada de seguimiento'),
            ('Recordatorio de tarea', 'Recordatorio de tarea'),
            ('Preparar sesión', 'Preparar sesión'),
            ('Enviar Email', 'Enviar Email'),
            ('Otra Tarea', 'Otra Tarea')
        ],
        default='Otra Tarea',
        verbose_name="Tipo de Actividad"
    )
    descripcion = models.TextField(verbose_name="Descripción", default="Sin descripción")
    fecha_vencimiento = models.DateField(blank=True, null=True, verbose_name="Fecha de Vencimiento")
    estado_actividad = models.CharField(
        max_length=20,
        choices=[
            ('Pendiente', 'Pendiente'),
            ('Completada', 'Completada'),
            ('Cancelada', 'Cancelada')
        ],
        default='Pendiente',
        verbose_name="Estado de Actividad"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    class Meta:
        verbose_name = "Actividad"
        verbose_name_plural = "Actividades"
        ordering = ['estado_actividad', 'fecha_vencimiento']

    def __str__(self):
        return f"Actividad: {self.descripcion[:50]} (Estado: {self.estado_actividad})"

class DocumentoPaciente(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='documentos')
    nombre = models.CharField(max_length=255)
    archivo = models.FileField(upload_to='documentos_pacientes/')
    fecha_subida = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.paciente}"

class Cita(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    estado = models.CharField(
        max_length=20,
        choices=[
            ('pendiente', 'Pendiente'),
            ('confirmada', 'Confirmada'),
            ('cancelada', 'Cancelada'),
            ('completada', 'Completada'),
        ],
        default='pendiente'
    )
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Cita con {self.paciente} el {self.fecha.strftime('%d/%m/%Y %H:%M')}"

class HistorialCambios(models.Model):
    modelo = models.CharField(max_length=100)
    objeto_id = models.CharField(max_length=100)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    cambio = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Historial cambio"
        verbose_name_plural = "Historial cambios"

class Consentimiento(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha_firma = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=100, choices=[('general', 'General'), ('psicoterapia', 'Psicoterapia')])
    firmado_por = models.CharField(max_length=255)
    archivo_pdf = models.FileField(upload_to='consentimientos/')

# --- Modelos de Marketing y Trazabilidad ---
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
        'Paciente',
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

class InteraccionMarketing(models.Model):
    paciente_potencial = models.ForeignKey(PacientePotencial, on_delete=models.CASCADE, related_name='interacciones')
    fecha_interaccion = models.DateTimeField(auto_now_add=True)
    tipo_interaccion = models.CharField(
        max_length=50,
        choices=[
            ('Llamada', 'Llamada'),
            ('Mensaje WhatsApp', 'Mensaje WhatsApp'),
            ('Email', 'Email'),
            ('Reunión', 'Reunión'),
            ('Otro', 'Otro'),
        ]
    )
    notas = models.TextField(blank=True, null=True, verbose_name="Notas / Detalles")

    def __str__(self):
        return f"{self.tipo_interaccion} con {self.paciente_potencial} el {self.fecha_interaccion.strftime('%d/%m/%Y %H:%M')}"

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
    paciente = models.ForeignKey('Paciente', on_delete=models.SET_NULL, blank=True, null=True, related_name='mensajes_bot')

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
        return f"{self.nombre} - {self.get_tipo_display()} - {self.fecha_cumpleanos.strftime('%d/%m')}"
