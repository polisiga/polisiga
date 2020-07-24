from django.urls import path

from . import views

app_name = 'academico'

urlpatterns = [
    path('',views.index, name='index'),
    path('alumno/', views.alumno_list, name='alumno_list'),
    path('alumno/<int:pk>/', views.alumno_detail, name='alumno_detail'),
    path('asignatura/', views.AsignaturaTableView.as_view(), name='asignatura_table_view'),
    path('asignatura_list/', views.asignatura_list_view, name='asignatura_list_view'),
    path('asignatura/<int:pk>/', views.asignatura_detail_view, name='asignatura_detail_view'),
    path('catedra/<int:pk>/', views.catedra_detail, name='catedra_detail'),
    path('docente/', views.docente_list, name='docente_list'),
    path('docente/<int:pk>/', views.docente_detail, name='docente_detail')
]
