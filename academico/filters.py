import django_filters

from .models import (
    Asignatura
)


class AsignaturaFilter(django_filters.FilterSet):

    nombre = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Asignatura
        fields = ['nombre']