# prm_salud/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('consultorio/', include('prm_salud.consultorio.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='consultorio/auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('', RedirectView.as_view(url='/consultorio/', permanent=False)),
]
