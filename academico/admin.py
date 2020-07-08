from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (
    Alumno,
    Asignatura,
    Departamento
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
    resource_class = AsignaturaResource


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    pass

