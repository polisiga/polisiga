from django.urls import reverse
import django_tables2 as tables
from django_tables2.utils import A
from django.utils.safestring import mark_safe

from .models import Asignatura

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