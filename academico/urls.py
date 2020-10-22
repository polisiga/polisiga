from django.urls import path

from . import views

from .views import CarreraListView
from .views import CarreraDetailView
from .views import CarreraAsignaturaView
from .views import CarreraCatedraView


app_name = 'academico'

urlpatterns = [
    path('',views.index, name='index'),
    path('alumno/', views.alumno_list, name='alumno_list'),
    path('alumno/<int:pk>/', views.alumno_detail, name='alumno_detail'),
    path('asignatura/', views.AsignaturaTableView.as_view(), name='asignatura_list'),
    path('asignatura/<int:pk>/', views.asignatura_detail_view, name='asignatura_detail_view'),
    path('asignatura/<int:pk>/plan/', views.AsignaturaPlanView.as_view(), name='asignatura_plan_list'),
    path('carrera/', CarreraListView.as_view(), name="carrera_list"),
    path('carrera/<int:pk>/', CarreraDetailView.as_view(), name='carrera_detail'),
    path('carrera/<int:pk>/asignatura/', CarreraAsignaturaView.as_view(), name='carrera_asignatura_list'),
    path('carrera/<int:pk>/catedra/', CarreraCatedraView.as_view(), name='carrera_catedra_list'),
    path('catedra/',views.CatedraView.as_view(), name='catedra_list'),
    path('catedra/<int:pk>/', views.catedra_detail_view, name='catedra_detail_view'),
    path('catedra/<int:catedra_pk>/registrocatedra/create/', views.registrocatedra_create_view, name='registrocatedra_create_view'),
    path('docente/', views.DocenteListView.as_view(), name='docente_list'),
    path('docente/<int:pk>/', views.docente_detail, name='docente_detail'),
    path('docente/<int:pk>/update/', views.DocenteUpdateView.as_view(), name='docente_update'),
    path('docente/<int:pk>/catedra/',views.DocenteCatedraView.as_view(), name='docente_catedra_list'),
    path('documento/',views.DocumentoListView.as_view(), name='documento_list'),
    path('documento/create/', views.DocumentoCreateView.as_view(), name='documento_create'),
    path('documento/<int:pk>/', views.DocumentoDetailView.as_view(), name='documento_detail'),
    path('documento/<int:pk>/update/', views.DocumentoUpdateView.as_view(), name='documento_update'),
    path('registrocatedra/<int:pk>/', views.registrocatedra_detail_view, name='registrocatedra_detail_view'),
    path('registrocatedra/<int:pk>/edit/', views.registrocatedra_edit_view, name='registrocatedra_edit_view')

]
