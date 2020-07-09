from django.contrib.auth.decorators import (
    login_required,
    permission_required)
from django.shortcuts import (
    get_object_or_404,
    render)


@login_required
def index(request):
    return render(request, 'academico/index.html')


def alumno_detail(request, pk):
    print("Hola " + str(pk))
    
    return render(request, 'academico/alumno_detail.html')

@login_required
@permission_required('view_alumno')
def alumno_list(request):
    print("prueba")
    return render(request, 'academico/alumno_list.html')


def asignatura_detail(request, pk):
    return render(request, 'academico/asignatura_detail.html')

def asignatura_list(request):
    return render(request, 'academico/asignatura_list.html')

def carrera_detail(request, pk):
    return render(request, 'academico/carrera_detail.html')

def carrera_list(request):
    return render(request, 'academico/carrera_list.html')   

def catedra_detail(request, pk):
    return render(request, 'academico/catedra_detail.html')

def catedra_list(request):
    return render(request, 'academico/catedra_list.html')

def contenido_detail(request, pk):
    return render(request, 'academico/contenido_detail.html')

def contenido_list(request):
    return render(request, 'academico/contenido_list.html')

def departamento_detail(request, pk):
    return render(request, 'academico/departamento_detail.html')

def departamento_list(request):
    return render(request, 'academico/departamento_list.html')

def docente_detail(request, pk):
    return render(request, 'academico/docente_detail.html')

def docente_list(request):
    return render(request, 'academico/docente_list.html')

def enfasis_detail(request, pk):
    return render(request, 'academico/enfasis_detail.html')

def enfasis_list(request):
    return render(request, 'academico/enfasis_list.html')

def grupo_homologas_detail(request, pk):
    return render(request, 'academico/grupo_homologas_detail.html')

def grupo_homologas_list(request):
    return render(request, 'academico/grupo_homologas_list.html')

def horario_detail(request, pk):
    return render(request, 'academico/horario_detail.html')

def horario_list(request):
    return render(request, 'academico/horario_list.html')

def periodo_detail(request, pk):
    return render(request, 'academico/periodo_detail.html')

def periodo_list(request):
    return render(request, 'academico/periodo_list.html')

def plan_detail(request, pk):
    return render(request, 'academico/plan_detail.html')

def plan_list(request):
    return render(request, 'academico/plan_list.html')

def registro_catedra_detail(request, pk):
    return render(request, 'academico/registro_catedra_detail.html')

def registro_catedra_list(request):
    return render(request, 'academico/registro_catedra_list.html')