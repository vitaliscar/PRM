from django.contrib import admin
from .models import PacientePotencial, InteraccionMarketing, RedSocial, BotWhatsappMensaje, CalendarioCumpleanos

# Unregister all previously registered models in the admin site
admin.site.unregister(PacientePotencial)
admin.site.unregister(InteraccionMarketing)
admin.site.unregister(RedSocial)
admin.site.unregister(BotWhatsappMensaje)
admin.site.unregister(CalendarioCumpleanos)
