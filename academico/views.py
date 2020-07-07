from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin)
from django.shortcuts import (
    get_object_or_404,
    render)

from django.views.generic import TemplateView

class HomeView(LoginRequiredMixin, TemplateView):
    """
    Aakmdslasasdlkasdmalsd
    Permisos: 'secretaria-academico' , 'dir-academico' 'jefe-departamento'
    """
    template_name = 'academico/index.html'

def index(request):
    return render(request, 'academico/index.html')


def alumno_list(request):
    return render(request, 'academico/alumno_list.html')

def alumno_detail(request):
    pass



