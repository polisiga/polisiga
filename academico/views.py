from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.shortcuts import render

from django.views.generic import TemplateView

class HomeView(LoginRequiredMixin, TemplateView):
    """
    Aakmdslasasdlkasdmalsd
    Permisos: Tiene q tener permiso 'visor-inicio'    
    """
    template_name = 'academico/index.html'

class AlumnoCrear(LoginRequiredMixin, TemplateView):
    
    pass

