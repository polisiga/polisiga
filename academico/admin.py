"""Pagina administrativa"""
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin


from .models import (
    Alumno,
    Asignatura,
    Carrera,
    Catedra,
    Contenido,
    Departamento,
    Docente,
    Enfasis,
    GrupoHomologas,
    Plan,
    Periodo,
    RegistroCatedra,

)

from .forms import (
    CatedraForm
)


User = get_user_model()


class DocenteInline(admin.StackedInline):
    """Docstring"""
    model = Docente
    can_delete = False


class UserAdmin(BaseUserAdmin):
    """Docstring"""
    inlines = [DocenteInline]


admin.site.unregister(User)

admin.site.register(User, UserAdmin)


class AlumnoResource(resources.ModelResource):
    """Docstring"""
    class Meta:
        """Docstring"""
        model = Alumno


class AlumnoAdmin(ImportExportModelAdmin):
    """Docstring"""
    resource_class = AlumnoResource


admin.site.register(Alumno, AlumnoAdmin)


class AsignaturaResource(resources.ModelResource):
    """Docstring"""
    class Meta:
        """Docstring"""
        model = Asignatura


@admin.register(Asignatura)
class AsignaturaAdmin(ImportExportModelAdmin):
    """Docstring"""
    list_display = (
        'id', 'codigo', 'grupohomologas',
        'siglas', 'nombre', 'carrera', 'departamento')
    search_fields = ('id', 'codigo', 'siglas', 'nombre')
    resource_class = AsignaturaResource


@admin.register(Carrera)
class CarreraAdmin(ImportExportModelAdmin):
    """Docstring"""


@admin.register(Catedra)
class CatedraAdmin(ImportExportModelAdmin):
    """Docstring"""
    form = CatedraForm

    autocomplete_fields = [
        'docentes',
        'asignaturas',
    ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(CatedraAdmin, self).get_form(request, **kwargs)
        # qs = Asignatura.objects.filter(pk=3)
        # form.base_fields['asignaturas'].queryset = qs
        return form


@admin.register(Contenido)
class ContenidoAdmin(ImportExportModelAdmin):
    """Docstring"""


@admin.register(Departamento)
class DepartamentoAdmin(ImportExportModelAdmin):
    """Docstring"""


@admin.register(Docente)
class DocenteAdmin(ImportExportModelAdmin):
    """Docstring"""
    search_fields = [
        'nombre',
        'apellido'
    ]
    autocomplete_fields = [
        'user',
    ]


class AsignaturaInLine(admin.TabularInline):
    """Docstring"""
    model = Asignatura
    fields = [
        'id',
        'codigo',
        'siglas',
        'nombre',
        'carrera',
        'departamento'
    ]

    readonly_fields = [
        'id',
        'codigo',
        'siglas',
        'nombre',
        'carrera',
        'departamento'
    ]

    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj):
        return False


@admin.register(Enfasis)
class EnfasisAdmin(ImportExportModelAdmin):
    """Docstring"""


@admin.register(GrupoHomologas)
class GrupoHomologasAdmin(ImportExportModelAdmin):
    """Docstring"""
    inlines = [
        AsignaturaInLine,
    ]


@admin.register(Periodo)
class PeriodoAdmin(ImportExportModelAdmin):
    """Docstring"""


class ContenidoInLine(admin.TabularInline):
    """Docstring"""
    model = Contenido


@admin.register(Plan)
class PlanAdmin(ImportExportModelAdmin):
    """Docstring"""
    autocomplete_fields = [
        'asignatura',
    ]
    inlines = [
        ContenidoInLine
    ]


@admin.register(RegistroCatedra)
class RegistroCatedraAdmin(ImportExportModelAdmin):
    """Docstring"""
