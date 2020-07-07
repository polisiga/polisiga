from django.contrib import admin

from .models import Alumno

# Register your models here.

class AlumnoAdmin(admin.ModelAdmin):
    pass

admin.site.register(Alumno, AlumnoAdmin)
