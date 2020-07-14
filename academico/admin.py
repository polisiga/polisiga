from django.contrib import admin
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

class AlumnoResource(resources.ModelResource):
    class Meta:
        model = Alumno

class AlumnoAdmin(ImportExportModelAdmin):
    resource_class = AlumnoResource

admin.site.register(Alumno, AlumnoAdmin)

class AsignaturaResource(resources.ModelResource):
    class Meta:
        model = Asignatura

@admin.register(Asignatura)
class AsignaturaAdmin(ImportExportModelAdmin):
    list_display = ('id', 'codigo','siglas','nombre')
    search_fields = ('id', 'codigo','siglas','nombre')
    resource_class = AsignaturaResource

@admin.register(Carrera)
class CarreraAdmin(ImportExportModelAdmin):
    pass

@admin.register(Catedra)
class CatedraAdmin(ImportExportModelAdmin):
    autocomplete_fields = [
        'docentes',
        'asignaturas'
    ]

@admin.register(Contenido)
class ContenidoAdmin(ImportExportModelAdmin):
    pass

@admin.register(Departamento)
class DepartamentoAdmin(ImportExportModelAdmin):
    pass

@admin.register(Docente)
class DocenteAdmin(ImportExportModelAdmin):
    search_fields = [
        'nombre',
        'apellido'
    ]

class AsignaturaInLine(admin.TabularInline):
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
    pass

@admin.register(GrupoHomologas)
class GrupoHomologasAdmin(ImportExportModelAdmin):
    inlines = [
        AsignaturaInLine,
    ]

@admin.register(Periodo)
class PeriodoAdmin(ImportExportModelAdmin):
    pass

class ContenidoInLine(admin.TabularInline):
    model = Contenido

@admin.register(Plan)
class PlanAdmin(ImportExportModelAdmin):
    autocomplete_fields = [
        'asignatura',
    ]
    inlines = [
        ContenidoInLine
    ]

@admin.register(RegistroCatedra)
class RegistroCatedraAdmin(ImportExportModelAdmin):
    pass