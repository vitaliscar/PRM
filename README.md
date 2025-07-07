# PRM Salud - Gestión Integral de Consultorio Psicológico

## Descripción General
PRM Salud es una plataforma web desarrollada en Django para la gestión integral de un consultorio psicológico. Permite administrar pacientes, profesionales, sesiones, notas clínicas, actividades, documentos, marketing, historial de cambios, consentimientos y más, con una interfaz moderna basada en Tailwind CSS y Flatpickr.

## Estructura del Proyecto
- **Backend:** Django 5.x
- **Frontend:** Tailwind CSS, integración de Flatpickr para fechas
- **Apps principales:**
  - `consultorio`: Gestión de pacientes, profesionales, sesiones, notas, actividades, documentos, citas, historial, consentimientos.
  - `marketing`: Gestión de pacientes potenciales, interacciones, redes sociales, bot WhatsApp, cumpleaños.
- **Base de datos:** SQLite (por defecto, configurable)
- **Dependencias clave:** `widget_tweaks`, `django-taggit`

## Funcionalidades
- **Pacientes:** Registro, edición, historial, documentos, consentimiento, citas.
- **Profesionales:** Gestión de usuarios profesionales.
- **Sesiones:** Agendamiento, edición, detalle, notas clínicas S.O.A.P., resumen IA.
- **Notas de sesión:** Formato S.O.A.P., integración con IA para resumen, historial.
- **Planes terapéuticos y actividades:** Registro, seguimiento y gestión.
- **Documentos:** Subida y gestión de archivos asociados a pacientes.
- **Citas:** Agendamiento y control de citas.
- **Historial de cambios:** Auditoría de acciones relevantes.
- **Consentimientos:** Gestión de consentimientos informados.
- **Marketing:** Seguimiento de pacientes potenciales, interacciones, redes sociales, campañas y cumpleaños.
- **Gestión de usuarios:** Roles, permisos y administración de usuarios.

## Funcionalidades por entidad

### Pacientes
- Registro y edición de datos personales, contacto y ficha clínica.
- Visualización de historial de sesiones, citas, documentos y consentimientos.
- Subida y gestión de documentos asociados.
- Consulta de próximas citas y sesiones pasadas.
- Eliminación lógica (conservando historial).

### Profesionales
- Alta, edición y baja de profesionales del consultorio.
- Asignación de sesiones y actividades.
- Control de permisos y roles (admin, psicólogo, asistente).

### Sesiones
- Agendamiento de nuevas sesiones con selección de paciente y profesional.
- Edición y reprogramación de sesiones.
- Visualización de detalle de sesión (fecha, hora, estado, profesional, paciente).
- Cancelación y registro de motivo de cancelación.
- Acceso directo a notas clínicas asociadas.

### Notas de Sesión
- Registro de notas clínicas en formato S.O.A.P. (Subjetivo, Objetivo, Análisis, Plan).
- Generación automática de resumen con IA (Gemini API).
- Historial y edición de notas por sesión.
- Valoración subjetiva y objetiva del progreso.

### Planes Terapéuticos
- Creación y seguimiento de planes de tratamiento para pacientes.
- Relación con sesiones y actividades.
- Edición y cierre de planes.

### Actividades
- Registro de tareas y recordatorios asociados a pacientes o profesionales.
- Seguimiento de estado y vencimiento.
- Visualización en dashboard y detalle de paciente.

### Documentos
- Subida, descarga y eliminación de archivos clínicos o administrativos.
- Asociación a pacientes y control de permisos.

### Citas
- Agendamiento, edición y cancelación de citas.
- Visualización de próximas citas y citas pasadas.
- Relación con pacientes y profesionales.

### Historial de Cambios
- Auditoría de acciones relevantes en el sistema.
- Visualización de cambios por entidad y usuario.

### Consentimientos
- Registro y gestión de consentimientos informados de pacientes.
- Descarga e historial de consentimientos firmados.

### Marketing y Trazabilidad
- Gestión de pacientes potenciales y su conversión.
- Registro de interacciones de marketing (llamadas, emails, etc.).
- Gestión de redes sociales y campañas.
- Envío y registro de mensajes automáticos por WhatsApp.
- Control y felicitación de cumpleaños de pacientes.

### Usuarios y Seguridad
- Gestión de usuarios, roles y permisos.
- Solicitud y aprobación de nuevos usuarios.
- Edición de perfil y cambio de contraseña.

## Lógica de funcionamiento

El sistema está diseñado para que los distintos roles (administrador, psicólogo, asistente) gestionen de forma segura y eficiente la información clínica y administrativa del consultorio. A continuación se describe el flujo general y la interacción entre las entidades principales:

1. **Gestión de usuarios y roles**
   - El administrador crea y gestiona usuarios, asignando roles y permisos.
   - Los usuarios pueden solicitar acceso y el administrador aprueba o rechaza.
   - Cada rol tiene acceso a diferentes funcionalidades según permisos.

2. **Registro y administración de pacientes**
   - Se registran pacientes con datos personales y clínicos.
   - Se pueden adjuntar documentos y gestionar consentimientos informados.
   - El historial del paciente muestra sesiones, citas, documentos y consentimientos asociados.

3. **Agendamiento y gestión de sesiones**
   - Los profesionales o asistentes agendan sesiones, seleccionando paciente, profesional, fecha y hora.
   - Las sesiones pueden ser editadas, reprogramadas o canceladas (con motivo).
   - Cada sesión puede tener una nota clínica asociada (formato S.O.A.P.), que puede ser editada y resumida con IA.

4. **Notas clínicas y seguimiento**
   - El profesional registra la nota de sesión, valorando el progreso y generando un resumen automático si lo desea.
   - Las notas quedan asociadas a la sesión y al paciente, y pueden ser consultadas en cualquier momento.

5. **Planes terapéuticos y actividades**
   - Se pueden crear planes de tratamiento para cada paciente, vinculando actividades y sesiones.
   - Las actividades pueden ser tareas, recordatorios o hitos, y se visualizan en el dashboard y en el detalle del paciente.

6. **Citas y recordatorios**
   - El sistema permite agendar citas independientes de las sesiones, útiles para controles, seguimientos u otros motivos.
   - Las próximas citas y sesiones se muestran en el perfil del paciente y en el dashboard.

7. **Documentos y consentimientos**
   - Se pueden subir documentos clínicos o administrativos, asociados a pacientes.
   - Los consentimientos informados se gestionan y almacenan para cada paciente.

8. **Marketing y trazabilidad**
   - Se registran pacientes potenciales y se hace seguimiento de su conversión.
   - Se gestionan interacciones de marketing, campañas, redes sociales y mensajes automáticos (WhatsApp).
   - El sistema recuerda y felicita cumpleaños de pacientes.

9. **Historial de cambios y auditoría**
   - Todas las acciones relevantes quedan registradas en el historial de cambios para auditoría y trazabilidad.

10. **Seguridad y privacidad**
    - El acceso a la información está restringido por roles y permisos.
    - Los datos sensibles se gestionan conforme a buenas prácticas de privacidad y protección de datos.

Este flujo asegura que la información esté centralizada, sea trazable y accesible solo para los usuarios autorizados, facilitando la gestión clínica y administrativa del consultorio.

## Estilos y experiencia visual

El sistema utiliza una combinación de Tailwind CSS, Flatpickr y personalizaciones propias para lograr una experiencia visual moderna, clara y coherente en todas las vistas.

### Tailwind CSS
- **Framework principal de estilos:** Todas las plantillas usan clases utilitarias de Tailwind para lograr un diseño responsivo, limpio y profesional.
- **Consistencia visual:** Los formularios, botones, tarjetas y tablas mantienen una apariencia uniforme gracias a la reutilización de clases Tailwind.
- **Colores personalizados:** Se han definido colores específicos para acciones principales (verde #9ae165 para guardar, azul para editar, rojo para eliminar) y para resaltar secciones clave.
- **Componentes reutilizables:** Se emplean layouts base (`base.html`) y componentes visuales reutilizables para mantener la coherencia.

### Flatpickr
- **Selección de fechas:** Los campos de fecha (como `fecha_nacimiento` o `fecha_sesion`) usan Flatpickr para una experiencia de usuario intuitiva y validación visual del formato.
- **Formato ISO:** Se fuerza el formato `YYYY-MM-DD` para compatibilidad y claridad.
- **Integración en plantillas:** El CSS y JS de Flatpickr se incluyen solo donde es necesario, evitando sobrecarga global.

### Personalización y detalles
- **widget_tweaks:** Se utiliza para añadir clases Tailwind a los campos de formularios generados por Django, asegurando que todos los inputs, selects y textareas tengan el mismo estilo.
- **Botones:** El botón de guardar/actualizar tiene color verde personalizado y sombra, con transición suave al pasar el mouse. Los botones de editar y eliminar usan azul y rojo respectivamente.
- **Tablas y tarjetas:** Las tablas de listados y las tarjetas de detalle usan bordes redondeados, sombras y colores de fondo suaves para mejorar la legibilidad.
- **Responsive:** Todo el sistema es usable en escritorio y dispositivos móviles.
- **Accesibilidad:** Se cuida el contraste y el tamaño de fuente para facilitar la lectura.

### Archivos y estructura
- El archivo principal de estilos globales es `main.css` (si existe), donde se pueden añadir reglas personalizadas.
- Los estilos de Tailwind se aplican directamente en las plantillas mediante clases.
- Flatpickr se integra en los templates de formularios que requieren selección de fecha.

Esta combinación permite que el sistema sea visualmente atractivo, fácil de usar y adaptable a las necesidades del consultorio.

## Guía rápida para modificar los estilos

1. **Modificar colores, fuentes o espaciados globales**
   - Edita el archivo `main.css` (si existe) para agregar o sobreescribir reglas CSS personalizadas.
   - Puedes añadir clases propias y usarlas en las plantillas junto con las de Tailwind.

2. **Cambiar la paleta de colores de Tailwind**
   - Si usas un archivo de configuración de Tailwind (`tailwind.config.js`), edita la sección `theme.colors` para personalizar colores globales.
   - Tras modificar la configuración, recompila los estilos si usas un build system (por ejemplo, `npm run build` o similar).

3. **Personalizar componentes visuales**
   - Modifica las clases Tailwind directamente en las plantillas HTML/Django para cambiar la apariencia de botones, tarjetas, tablas, etc.
   - Ejemplo: para cambiar el color del botón de guardar, edita la clase en el template correspondiente.

4. **Modificar el estilo de Flatpickr**
   - Puedes sobreescribir estilos de Flatpickr en `main.css` o importar un tema diferente de Flatpickr en los templates.
   - Consulta la [documentación oficial de Flatpickr](https://flatpickr.js.org/themes/) para ver temas disponibles.

5. **Agregar o cambiar iconos**
   - Si usas una librería de iconos (como Lucide o FontAwesome), puedes cambiar los íconos modificando las etiquetas `<i>` o `<svg>` en los templates.

6. **Responsive y accesibilidad**
   - Usa las utilidades de Tailwind (`sm:`, `md:`, `lg:`) para adaptar el diseño a diferentes dispositivos.
   - Verifica el contraste y el tamaño de fuente para mantener la accesibilidad.

7. **Prueba visual**
   - Tras cualquier cambio, revisa la app en diferentes navegadores y dispositivos para asegurar la coherencia visual.

> Si tienes dudas sobre cómo aplicar un cambio visual específico, revisa primero la plantilla correspondiente en `prm_salud/consultorio/templates/consultorio/` y busca las clases Tailwind o reglas CSS aplicadas.

## Estructura de Carpetas
```
PRM/
├── db.sqlite3
├── manage.py
├── README.md
├── requirements.txt
├── prm_salud/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── consultorio/
│       ├── models.py
│       ├── views.py
│       ├── forms.py
│       ├── urls.py
│       ├── templates/
│       │   └── consultorio/
│       │       ├── pacientes/
│       │       ├── sesiones/
│       │       ├── notas/
│       │       ├── profesionales/
│       │       ├── actividades/
│       │       ├── documentos/
│       │       ├── citas/
│       │       ├── historial/
│       │       ├── consentimientos/
│       │       ├── marketing/
│       │       └── base.html
│       └── ...
│   └── marketing/
│       ├── models.py
│       ├── views.py
│       ├── forms.py
│       ├── urls.py
│       └── ...
└── ...
```

## Instalación rápida
1. Clona el repositorio y entra al directorio del proyecto.
2. Crea y activa un entorno virtual:
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Instala dependencias:
   ```powershell
   pip install -r requirements.txt
   ```
4. Aplica migraciones:
   ```powershell
   python manage.py migrate
   ```
5. Ejecuta el servidor:
   ```powershell
   python manage.py runserver
   ```

## Notas técnicas
- El archivo de configuración principal es `prm_salud/settings.py`.
- Si ves errores de módulo `suite_prm`, revisa que la variable de entorno `DJANGO_SETTINGS_MODULE` esté en `prm_salud.settings`.
- Las plantillas están en `prm_salud/consultorio/templates/consultorio/`.
- Los formularios usan `widget_tweaks` para personalización de clases CSS.
- Flatpickr se integra en los templates para campos de fecha.
- El namespace principal de URLs es `consultorio`.

## Pendiente
- Validación visual final de formularios y botones en todos los navegadores.
- Mejorar documentación de endpoints, estructura de modelos y ejemplos de uso.

---
Actualizado: julio 2025
