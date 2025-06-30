# urls.py para prm_salud
from django.urls import path, include

urlpatterns = [
    # ...existing code...
    path('consultorio/', include('consultorio.urls')),
    # ...existing code...
]
