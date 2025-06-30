from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import PacientePotencial, InteraccionMarketing, RedSocial, BotWhatsappMensaje, CalendarioCumpleanos
from .forms import PacientePotencialForm, InteraccionMarketingForm, RedSocialForm, BotWhatsappMensajeForm, CalendarioCumpleanosForm

# PacientePotencial
class PacientePotencialListView(ListView):
    model = PacientePotencial
    template_name = 'consultorio/marketing/pacientepotencial_list.html'

class PacientePotencialDetailView(DetailView):
    model = PacientePotencial
    template_name = 'consultorio/marketing/pacientepotencial_detail.html'

class PacientePotencialCreateView(CreateView):
    model = PacientePotencial
    form_class = PacientePotencialForm
    template_name = 'consultorio/marketing/pacientepotencial_form.html'
    success_url = reverse_lazy('pacientepotencial_list')

class PacientePotencialUpdateView(UpdateView):
    model = PacientePotencial
    form_class = PacientePotencialForm
    template_name = 'consultorio/marketing/pacientepotencial_form.html'
    success_url = reverse_lazy('pacientepotencial_list')

class PacientePotencialDeleteView(DeleteView):
    model = PacientePotencial
    template_name = 'consultorio/marketing/pacientepotencial_confirm_delete.html'
    success_url = reverse_lazy('pacientepotencial_list')

# InteraccionMarketing
class InteraccionMarketingListView(ListView):
    model = InteraccionMarketing
    template_name = 'consultorio/marketing/interaccionmarketing_list.html'

class InteraccionMarketingDetailView(DetailView):
    model = InteraccionMarketing
    template_name = 'consultorio/marketing/interaccionmarketing_detail.html'

class InteraccionMarketingCreateView(CreateView):
    model = InteraccionMarketing
    form_class = InteraccionMarketingForm
    template_name = 'consultorio/marketing/interaccionmarketing_form.html'
    success_url = reverse_lazy('interaccionmarketing_list')

class InteraccionMarketingUpdateView(UpdateView):
    model = InteraccionMarketing
    form_class = InteraccionMarketingForm
    template_name = 'consultorio/marketing/interaccionmarketing_form.html'
    success_url = reverse_lazy('interaccionmarketing_list')

class InteraccionMarketingDeleteView(DeleteView):
    model = InteraccionMarketing
    template_name = 'consultorio/marketing/interaccionmarketing_confirm_delete.html'
    success_url = reverse_lazy('interaccionmarketing_list')

# RedSocial
class RedSocialListView(ListView):
    model = RedSocial
    template_name = 'consultorio/marketing/redsocial_list.html'

class RedSocialDetailView(DetailView):
    model = RedSocial
    template_name = 'consultorio/marketing/redsocial/redsocial_detail.html'

class RedSocialCreateView(CreateView):
    model = RedSocial
    form_class = RedSocialForm
    template_name = 'consultorio/marketing/redsocial/redsocial_form.html'
    success_url = reverse_lazy('redsocial_list')

class RedSocialUpdateView(UpdateView):
    model = RedSocial
    form_class = RedSocialForm
    template_name = 'consultorio/marketing/redsocial/redsocial_form.html'
    success_url = reverse_lazy('redsocial_list')

class RedSocialDeleteView(DeleteView):
    model = RedSocial
    template_name = 'consultorio/marketing/redsocial/redsocial_confirm_delete.html'
    success_url = reverse_lazy('redsocial_list')

# BotWhatsappMensaje
class BotWhatsappMensajeListView(ListView):
    model = BotWhatsappMensaje
    template_name = 'consultorio/marketing/botwhatsappmensaje/botwhatsappmensaje_list.html'

class BotWhatsappMensajeDetailView(DetailView):
    model = BotWhatsappMensaje
    template_name = 'consultorio/marketing/botwhatsappmensaje/botwhatsappmensaje_detail.html'

class BotWhatsappMensajeCreateView(CreateView):
    model = BotWhatsappMensaje
    form_class = BotWhatsappMensajeForm
    template_name = 'consultorio/marketing/botwhatsappmensaje/botwhatsappmensaje_form.html'
    success_url = reverse_lazy('botwhatsappmensaje_list')

class BotWhatsappMensajeUpdateView(UpdateView):
    model = BotWhatsappMensaje
    form_class = BotWhatsappMensajeForm
    template_name = 'consultorio/marketing/botwhatsappmensaje/botwhatsappmensaje_form.html'
    success_url = reverse_lazy('botwhatsappmensaje_list')

class BotWhatsappMensajeDeleteView(DeleteView):
    model = BotWhatsappMensaje
    template_name = 'consultorio/marketing/botwhatsappmensaje/botwhatsappmensaje_confirm_delete.html'
    success_url = reverse_lazy('botwhatsappmensaje_list')

# CalendarioCumpleanos
class CalendarioCumpleanosListView(ListView):
    model = CalendarioCumpleanos
    template_name = 'consultorio/marketing/calendariocumpleanos/calendariocumpleanos_list.html'

class CalendarioCumpleanosDetailView(DetailView):
    model = CalendarioCumpleanos
    template_name = 'consultorio/marketing/calendariocumpleanos/calendariocumpleanos_detail.html'

class CalendarioCumpleanosCreateView(CreateView):
    model = CalendarioCumpleanos
    form_class = CalendarioCumpleanosForm
    template_name = 'consultorio/marketing/calendariocumpleanos/calendariocumpleanos_form.html'
    success_url = reverse_lazy('calendariocumpleanos_list')

class CalendarioCumpleanosUpdateView(UpdateView):
    model = CalendarioCumpleanos
    form_class = CalendarioCumpleanosForm
    template_name = 'consultorio/marketing/calendariocumpleanos/calendariocumpleanos_form.html'
    success_url = reverse_lazy('calendariocumpleanos_list')

class CalendarioCumpleanosDeleteView(DeleteView):
    model = CalendarioCumpleanos
    template_name = 'consultorio/marketing/calendariocumpleanos/calendariocumpleanos_confirm_delete.html'
    success_url = reverse_lazy('calendariocumpleanos_list')
