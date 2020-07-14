from django.urls import reverse
import django_tables2 as tables
from django_tables2.utils import A
from django.utils.safestring import mark_safe

from .models import Asignatura

class AsignaturaTable(tables.Table):
    
    id = tables.Column(linkify=True)

    class Meta:
        model = Asignatura
        template_name = 'django_tables2/bootstrap4.html'
        fields = (
            'id',
            'codigo',
            'siglas',
            'nombre',
            'carrera',
            'departameto'
        )