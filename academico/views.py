from django.contrib.auth.decorators import (
    login_required,
    permission_required)
from django.shortcuts import (
    get_object_or_404,
    render)


@login_required
def index(request):
    return render(request, 'academico/index.html')


def alumno_detail(request):
    return render(request, 'academico/alumno_detail.html')

@login_required
@permission_required('view_alumno')
def alumno_list(request):
    return render(request, 'academico/alumno_list.html')


def asignatura_detail(request, pk):
    return render(request, 'academico/asignatura_detail.html')

def asignatura_list(request):
    return render(request, 'academico/asignatura_list.html')


def docente_detail(request, pk):
    return render(request, 'academico/asignatura_detail.html')

def docente_list(request):
    return render(request, 'academico/docente_list.html')