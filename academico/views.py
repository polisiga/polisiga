from django.contrib.auth.decorators import (
    login_required,
    permission_required,
)
from django.core.paginator import Paginator
from django.shortcuts import (
    get_list_or_404,
    get_object_or_404,
    redirect,
    render,
)
from django.utils import timezone
from datetime import timedelta
from datetime import date
from django_filters.views import FilterView
from django_tables2 import (
    SingleTableView,
    SingleTableMixin
)

from .filters import (
    AsignaturaFilter
)

from .forms import (
    RegistroCatedraForm
)
from .tables import (
    AsignaturaTable
)

from .models import (
    Asignatura,
    Catedra,
    Docente,
    Contenido,
    Alumno,
    Plan,
    RegistroCatedra,
)

@login_required
def index(request):


    return render(request, 'academico/index.html')

def index_redirect(request):
    return redirect('academico:index')


def alumno_detail(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)

    return render(request, 'academico/alumno_detail.html', {'alumno': alumno})

@login_required
@permission_required('view_alumno')
def alumno_list(request):
    alumnos = get_list_or_404(Alumno)
    return render(request, 'academico/alumno_list.html', {'alumnos': alumnos})


class AsignaturaTableView(SingleTableMixin, FilterView):
    model = Asignatura
    table_class = AsignaturaTable
    template_name = 'academico/asignatura_table_view.html'

    filterset_class = AsignaturaFilter

def asignatura_detail_view(request, pk):
    asignatura = get_object_or_404(Asignatura, pk=pk)

    return render(request, 'academico/asignatura_detail_view.html', {'asignatura': asignatura})

def asignatura_list_view(request, *args, **kwargs):


    asignatura_list = AsignaturaFilter(request.GET, queryset=Asignatura.objects.all())


    paginator = Paginator(asignatura_list.qs, 25)

    page = request.GET.get('page')
    asignaturas_page = paginator.get_page(page)

    return render(request, 'academico/asignatura_list_view.html',
                  {
                      'asignaturas_page': asignaturas_page,
                      'asignatura_list': asignatura_list,
                  })

def carrera_detail(request, pk):
    return render(request, 'academico/carrera_detail.html')

def carrera_list(request):
    return render(request, 'academico/carrera_list.html')   

# TODO: Validar que dias podria cargar un registrocatedra
def catedra_detail_view(request, pk):

    catedra = get_object_or_404(Catedra, pk=pk)
    return render(request, 'academico/catedra_detail_view.html', {'catedra': catedra})

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

def registrocatedra_detail_view(request, pk):
    registrocatedra = get_object_or_404(RegistroCatedra, pk=pk)
    return render(request, 'academico/registrocatedra_detail_view.html',{'registrocatedra': registrocatedra})

def registrocatedra_list_view(request):

    return render(request, 'academico/registrocatedra_list_view.html')

def registrocatedra_edit_view(request, pk):
    registrocatedra = get_object_or_404(RegistroCatedra, pk=pk)
    if request.method == 'POST':
        form = RegistroCatedraForm(request.POST, instance=registrocatedra)
        if form.is_valid():
            form.save()
            #form.save_m2m()
            return redirect('academico:registrocatedra_detail_view', pk=registrocatedra.pk)
    else:
        form = RegistroCatedraForm(instance=registrocatedra)
        form.fields['contenidos_desarrollados'].queryset = Contenido.objects.filter(
            plan=registrocatedra.plan_activo())
    return render(request, 'academico/registrocatedra_edit_view.html', {'form': form})

@login_required
@permission_required('academico.add_own_registrocatedra', raise_exception=True)
def registrocatedra_create_view(request, catedra_pk):
    """ Vista para cargar registro de Catedra. """
    catedra = Catedra.objects.get(pk=catedra_pk)
    plan = catedra.get_plan()
    if request.method == "POST":
        form = RegistroCatedraForm(request.POST)
        if form.is_valid():
            registrocatedra = form.save(commit=False)
            #post.author = request.user
            #post.published_date = timezone.now()
            #registrocatedra.catedra = catedra_pk
            #registrocatedra.docente = request.user.docente.pk
            registrocatedra.save()
            form.save_m2m()
            return redirect('academico:registrocatedra_detail_view', pk=registrocatedra.pk)
    else:
        form = RegistroCatedraForm()
        
        form.fields['catedra'].initial = catedra_pk
        form.fields['catedra'].queryset = Catedra.objects.filter(pk=catedra_pk)
        #form.fields['catedra'].widget.attrs['disabled'] = True

        
        form.fields['docente'].initial = request.user.docente.pk
        form.fields['docente'].queryset = Docente.objects.filter(pk=request.user.docente.pk)
        #form.fields['docente'].widget.attrs['disabled'] = True

        form.fields['contenidos_desarrollados'].queryset = Contenido.objects.filter(
            plan=catedra.get_plan())

    return render(request, 'academico/registrocatedra_create_view.html', {'form': form})