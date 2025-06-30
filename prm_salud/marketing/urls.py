from django.urls import path
from . import views

urlpatterns = [
    # PacientePotencial
    path('pacientepotencial/', views.PacientePotencialListView.as_view(), name='pacientepotencial_list'),
    path('pacientepotencial/<uuid:pk>/', views.PacientePotencialDetailView.as_view(), name='pacientepotencial_detail'),
    path('pacientepotencial/create/', views.PacientePotencialCreateView.as_view(), name='pacientepotencial_create'),
    path('pacientepotencial/<uuid:pk>/update/', views.PacientePotencialUpdateView.as_view(), name='pacientepotencial_update'),
    path('pacientepotencial/<uuid:pk>/delete/', views.PacientePotencialDeleteView.as_view(), name='pacientepotencial_delete'),

    # RedSocial
    path('redsocial/', views.RedSocialListView.as_view(), name='redsocial_list'),
    path('redsocial/<int:pk>/', views.RedSocialDetailView.as_view(), name='redsocial_detail'),
    path('redsocial/create/', views.RedSocialCreateView.as_view(), name='redsocial_create'),
    path('redsocial/<int:pk>/update/', views.RedSocialUpdateView.as_view(), name='redsocial_update'),
    path('redsocial/<int:pk>/delete/', views.RedSocialDeleteView.as_view(), name='redsocial_delete'),

    # BotWhatsappMensaje
    path('botwhatsappmensaje/', views.BotWhatsappMensajeListView.as_view(), name='botwhatsappmensaje_list'),
    path('botwhatsappmensaje/<int:pk>/', views.BotWhatsappMensajeDetailView.as_view(), name='botwhatsappmensaje_detail'),
    path('botwhatsappmensaje/create/', views.BotWhatsappMensajeCreateView.as_view(), name='botwhatsappmensaje_create'),
    path('botwhatsappmensaje/<int:pk>/update/', views.BotWhatsappMensajeUpdateView.as_view(), name='botwhatsappmensaje_update'),
    path('botwhatsappmensaje/<int:pk>/delete/', views.BotWhatsappMensajeDeleteView.as_view(), name='botwhatsappmensaje_delete'),

    # CalendarioCumpleanos
    path('calendariocumpleanos/', views.CalendarioCumpleanosListView.as_view(), name='calendariocumpleanos_list'),
    path('calendariocumpleanos/<int:pk>/', views.CalendarioCumpleanosDetailView.as_view(), name='calendariocumpleanos_detail'),
    path('calendariocumpleanos/create/', views.CalendarioCumpleanosCreateView.as_view(), name='calendariocumpleanos_create'),
    path('calendariocumpleanos/<int:pk>/update/', views.CalendarioCumpleanosUpdateView.as_view(), name='calendariocumpleanos_update'),
    path('calendariocumpleanos/<int:pk>/delete/', views.CalendarioCumpleanosDeleteView.as_view(), name='calendariocumpleanos_delete'),
]
