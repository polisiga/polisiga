from django.urls import reverse
from django.utils.html import format_html
import django_tables2 as tables
from django_tables2.utils import A
from django.utils.safestring import mark_safe

from .models import Asignatura
from .models import Docente
from .models import Documento

class AsignaturaTable(tables.Table):

    id = tables.Column(linkify=True)
    carrera = tables.Column('Carrera', accessor=A('carrera__siglas'))
    departamento = tables.Column('Dpto', accessor=A('departamento__siglas'))

    editar = tables.Column('editar', accessor=A('id'))


    def render_editar(self, value, record):
        return mark_safe('<span class="label label-success">Approved</span>')


    class Meta:
        model = Asignatura
        template_name = 'django_tables2/bootstrap4.html'
        fields = (
            'id',
            'codigo',
            'siglas',
            'nombre',
            'carrera',
            'departamento',
        )

class DocenteTable(tables.Table):

    id = tables.Column(linkify=True)


    editar = tables.Column('', accessor=A('id'))


    def render_editar(self, value, record):
        return format_html(
            '''
            <a href="{}" class="btn btn-primary" role="button"><i class="far fa-eye"></i></a>
            <a href="{}" class="btn btn-success" role="button"><i class="fas fa-pen"></i></a>
            ''',
            reverse('academico:docente_detail', args=[value]),
            reverse('academico:docente_update', args=[value]),
            )


    class Meta:
        model = Docente
        template_name = 'django_tables2/bootstrap4.html'
        fields = (
            'id',
            'cedula',
            'apellido',
            'nombre',
            'email'
        )


class DocumentoTable(tables.Table):

    id = tables.Column(linkify=True)


    editar = tables.Column('', accessor=A('id'))


    def render_editar(self, value, record):
        return format_html(
            '''
            <a href="{}" class="btn btn-primary" role="button"><i class="far fa-eye"></i></a>
            <a href="{}" class="btn btn-success" role="button"><i class="fas fa-pen"></i></a>
            ''',
            reverse('academico:documento_detail', args=[value]),
            reverse('academico:documento_update', args=[value]),
            )


    class Meta:
        model = Documento
        template_name = 'django_tables2/bootstrap4.html'
        fields = (
            'id',
            'fecha',
            'tipo',
            'descripcion',
        )
