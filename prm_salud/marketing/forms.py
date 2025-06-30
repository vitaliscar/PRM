from django import forms
from .models import PacientePotencial, InteraccionMarketing, RedSocial, BotWhatsappMensaje, CalendarioCumpleanos

class PacientePotencialForm(forms.ModelForm):
    class Meta:
        model = PacientePotencial
        fields = '__all__'

class InteraccionMarketingForm(forms.ModelForm):
    class Meta:
        model = InteraccionMarketing
        fields = '__all__'

class RedSocialForm(forms.ModelForm):
    class Meta:
        model = RedSocial
        fields = '__all__'

class BotWhatsappMensajeForm(forms.ModelForm):
    class Meta:
        model = BotWhatsappMensaje
        fields = '__all__'

class CalendarioCumpleanosForm(forms.ModelForm):
    class Meta:
        model = CalendarioCumpleanos
        fields = '__all__'
