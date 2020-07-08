from django.urls import path

from . import views

app_name = 'academico'

urlpatterns = [
    path('',views.index, name='index'),
    path('alumno/', views.alumno_list, name='alumno_list'),
    path('alumno/<int:pk>/', views.alumno_detail, name='alumno_detail'),
    path('asignatura/', views.asignatura_list, name='asignatura_list'),
    path('asignatura/<int:pk>/', views.asignatura_detail, name='asignatura_detail'),
    path('docente/', views.docente_list, name='docente_list'),
    path('docente/<int:pk>/', views.docente_detail, name='docente_detail')
]
