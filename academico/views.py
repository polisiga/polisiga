from django.contrib.auth.decorators import (
    login_required,
    permission_required,
)
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator

from django.shortcuts import (
    get_list_or_404,
    get_object_or_404,
    redirect,
    render,
)
from django.urls import reverse
from django.utils import timezone
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from datetime import timedelta
from datetime import date
from django_filters.views import FilterView
from django_tables2 import (
    SingleTableView,
    SingleTableMixin
)

from .filters import (
    AsignaturaFilter,
    CatedraFilter,
    DocenteFilter,
    DocumentoFilter
)

from .forms import (
    RegistroCatedraForm
)
from .tables import (
    AsignaturaTable,
    CatedraTable,
    CarreraTable,
    DocenteTable,
    DocumentoTable,
    PlanTable,
)

from .models import (
    Asignatura,
    Carrera,
    Catedra,
    Contenido,
    Docente,
    Documento,
    Estudiante,
    Plan,
    RegistroCatedra,
)

@login_required
def index(request):


    return render(request, 'academico/index.html',{'titulo': "Tablero"})

def index_redirect(request):
    return redirect('academico:index')


class AsignaturaTableView(SingleTableMixin, FilterView):
    model = Asignatura
    table_class = AsignaturaTable
    template_name = 'academico/asignatura_table_view.html'

    filterset_class = AsignaturaFilter

class AsignaturaPlanView(SingleTableView):
    model = Plan
    table_class = PlanTable
    #table = PlanTable(Plan.objects.filter(asignatura=))
    template_name = 'academico/asignatura_plan_list.html'
    

    def dispatch(self, request, *args, **kwargs):

        self.asignatura = Asignatura.objects.get(pk=self.kwargs['pk'])
        return super(AsignaturaPlanView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):

        return Plan.objects.filter(asignatura=self.asignatura)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context["titulo"] = "Planes de " + str(self.asignatura)
        context["asignatura"] = self.asignatura

        return context
        

class AsignaturaPlanDetailView(DetailView):
    model = Plan
    template_name = "academico/asignatura_plan_detail.html"

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

class CarreraListView(PermissionRequiredMixin, SingleTableView):
    permission_required = 'academico.view_carrera'
    table_class = CarreraTable
    model = Carrera
    template_name = 'academico/carrera_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Carreras"
        context['breadcrumbs'] = [
            {'value': "Inicio", 'url': reverse('academico:index')},
            {'value': "Carreras", 'active': True}
        ]
        return context

class CarreraDetailView(DetailView):
    model = Carrera

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Detalle de " + str(self.object)
        context['breadcrumbs'] = [
            {'value': "Inicio", 'url': reverse('academico:index')},
            {'value': "Carreras", 'url': reverse('academico:carrera_list')},
            {'value': str(self.object.siglas), 'active': True}
        ]
        return context


class CarreraAsignaturaView(PermissionRequiredMixin, SingleTableMixin, FilterView):
    permission_required = 'academico.view_asigntura'
    table_class = AsignaturaTable
    model = Asignatura
    template_name = 'academico/carrera_asignatura_list.html'
    filterset_class = AsignaturaFilter

    def get_queryset(self):
        self.carrera = Carrera.objects.get(pk=self.kwargs['pk'])
        qs = Asignatura.objects.filter(carrera=self.carrera)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context["titulo"] = "Asignaturas de " + str(self.carrera)
        context['breadcrumbs'] = [
            {'value': "Inicio", 'url': reverse('academico:index')},
            {'value': "Carreras", 'url': reverse('academico:carrera_list')},
            {'value': str(self.carrera.siglas), 'url': reverse('academico:carrera_detail', args=[self.carrera.pk])},
            {'value': "Asignaturas", 'active': True}
        ]

        return context


class CarreraCatedraView(PermissionRequiredMixin, SingleTableView):
    permission_required = 'academico.view_catedra'
    table_class = CatedraTable
    model = Catedra
    template_name = 'academico/carrera_catedra_list.html'
    #filterset_class = CatedraFilter

    def get_queryset(self):
        self.carrera = Carrera.objects.get(pk=self.kwargs['pk'])
        #qs = Catedra.objects.filter(carrera=self.carrera)
        qs = Catedra.objects.filter(asignaturas__carrera=self.carrera)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context["titulo"] = "Asignaturas de " + str(self.carrera)
        context["breadcrumbs"] = [
            {'value': "Inicio", 'url': reverse('academico:index')},
            {'value': "Carreras", 'url': reverse('academico:carrera_list')},
            {'value': str(self.carrera.siglas), 'url': reverse('academico:carrera_detail', args=[self.carrera.pk])},
            {'value': "Catedras", 'active': True}
        ]

        return context




# TODO: Validar que dias podria cargar un registrocatedra
def catedra_detail_view(request, pk):

    catedra = get_object_or_404(Catedra, pk=pk)
    return render(request, 'academico/catedra_detail.html',
                    {
                        'catedra': catedra,
                        'docentes': catedra.docentes
                    
                    })

def catedra_list(request):
    return render(request, 'academico/catedra_list.html')

class CatedraView(PermissionRequiredMixin, SingleTableMixin, FilterView):
    permission_required = 'academico.view_catedra'
    table_class = CatedraTable
    model = Catedra
    template_name = 'academico/catedra_list.html'
    filterset_class = CatedraFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Catedras"
        return context

def contenido_detail(request, pk):
    return render(request, 'academico/contenido_detail.html')

def contenido_list(request):
    return render(request, 'academico/contenido_list.html')

def departamento_detail(request, pk):
    return render(request, 'academico/departamento_detail.html')

def departamento_list(request):
    return render(request, 'academico/departamento_list.html',{'titulo': "Docentes"})

def docente_detail(request, pk):
    docente = get_object_or_404(Docente, pk=pk)
    docente_catedra_set = docente.catedra_set.all()[:5]
    docente_documento_set = docente.documento_set.all()[:5]
    return render(
        request,
        'academico/docente_detail.html',
        {
            'titulo': "Detalle de docente " + str(docente),
            'docente': docente,
            'docente_catedra_set': docente_catedra_set,
            'docente_documento_set': docente_documento_set,
        }
    )

class DocenteUpdateView(UpdateView):
    model = Docente
    template_name = "academico/docente_update.html"
    fields = [
        'cedula',
        'apellido',
        'nombre',
        'email'
        ]

@permission_required('academico.view_docente')
def docente_list(request):

    docentes = DocenteFilter(request.GET, queryset=Docente.objects.all())
    paginator = Paginator(docentes.qs, 25)
    page = request.GET.get('page')
    docentes_page = paginator.get_page(page)

    return render(request, 'academico/docente_list.html',
                  {'docentes': docentes, 'docentes_page': docentes_page})

class DocenteListView(PermissionRequiredMixin, SingleTableMixin, FilterView):
    permission_required = 'academico.view_docente'
    table_class = DocenteTable
    model = Docente
    template_name = 'academico/docente_list.html'
    filterset_class = DocenteFilter

class DocenteCatedraView(PermissionRequiredMixin, SingleTableView):
    permission_required = 'academico.view_catedra'
    table_class = CatedraTable
    model = Catedra
    template_name = 'academico/docente_catedra_list.html'

    def get_queryset(self):
        self.docente = Docente.objects.get(pk=self.kwargs['pk'])
        qs = Catedra.objects.filter(docentes=self.docente)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context["titulo"] = "Catedras de " + str(self.docente)
        context["docente"] = self.docente
        context["breadcrumbs"] = [
            {'value': "Inicio", 'url': reverse('academico:index')},
            {'value': "Docentes", 'url': reverse('academico:docente_list')},
            {'value': str(self.docente.id), 'url': reverse('academico:docente_detail', args=[self.docente.pk])},
            {'value': "Catedras", 'active': True}
        ]
        return context
    


    

    def has_permission(self, *args, **kwargs):
        # si soy docente de la catedra se permite ver
        # o si se tiene el permiso view_catedra


        #se retorna True si se tiene permiso
        return True


class DocumentoListView(PermissionRequiredMixin, SingleTableMixin, FilterView):
    permission_required = 'academico.view_documento'
    table_class = DocumentoTable
    model = Documento
    template_name = 'academico/documento_list.html'
    filterset_class = DocumentoFilter


class DocumentoDetailView(DetailView):
    model = Documento


class DocumentoCreateView(SuccessMessageMixin, CreateView):
    model = Documento
    fields = [
        'tipo',
        'descripcion',
        'fecha',
        'nro_acta',
        'nro_res',
        'otra_numeracion',
        'docentes_relacionados',
        'url'
    ]
    template_name_suffix = '_create'
    success_message = "Documento creado exitosamente."


class DocumentoUpdateView(SuccessMessageMixin, UpdateView):
    model = Documento
    fields = [
        'tipo',
        'descripcion',
        'fecha',
        'nro_acta',
        'nro_res',
        'otra_numeracion',
        'docentes_relacionados',
        'url'
    ]
    template_name_suffix = '_update'
    success_message = "Documento actualizado exitosamente."


def enfasis_detail(request, pk):
    return render(request, 'academico/enfasis_detail.html')

def enfasis_list(request):
    return render(request, 'academico/enfasis_list.html')


def estudiante_detail(request, pk):
    estudiante = get_object_or_404(Estudiante, pk=pk)

    return render(request, 'academico/estudiante_detail.html', {'estudiante': estudiante})

@login_required
@permission_required('view_estudiante')
def estudiante_list(request):
    estudiantes = get_list_or_404(Estudianete)
    return render(request, 'academico/estudiante_list.html', {'estudiante': estudiante})

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
            messages.success(request, 'Registro de Catedra actualizado correctamente.')
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