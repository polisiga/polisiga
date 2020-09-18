import django_filters
from django.forms.widgets import TextInput

from .models import (
    Asignatura,
    Docente
)


class AsignaturaFilter(django_filters.FilterSet):

    nombre = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Asignatura
        fields = [
            'nombre',
            'carrera',
            'departamento',
            'semestre'
        ]

class DocenteFilter(django_filters.FilterSet):

    apellido = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=TextInput(attrs={'placeholder': 'Apellido contiene'}),
        )
    nombre = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=TextInput(attrs={'placeholder': 'Nombre contiene'}),
        )

    class Meta:
        model = Docente
        fields = [
            'cedula',
            'apellido',
            'nombre',
        ]