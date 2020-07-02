from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.shortcuts import render

from django.views.generic import TemplateView

class HomeView(LoginRequiredMixin, TemplateView):
    """
    Aakmdslasasdlkasdmalsd
    Permisos: 'secretaria-academico' , 'dir-academico' 'jefe-departamento'
    """
    template_name = 'academico/index.html'


class AlumnoCrear(LoginRequiredMixin, TemplateView):

    pass

class AlumnoListar(TemplateView):
    pass
