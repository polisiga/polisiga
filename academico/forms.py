from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, Field, Column

from .models import ( 
    Asignatura,
    Catedra,
    RegistroCatedra,
)

class CatedraForm(forms.ModelForm):

    
    class Meta:
        model = Catedra
        fields = [
            'descripcion',
            'docentes',
            'asignaturas',
            'periodo',
            'seccion',
            'fecha_desde',
            'fecha_hasta',
            'fecha_1par',
            'hora_1par',
            'fecha_2par',
            'hora_2par',
            'fecha_1final',
            'hora_1final',
            'fecha_2final',
            'hora_2final'
        ]

    def clean(self):
    
        return self.cleaned_data

class RegistroCatedraForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RegistroCatedraForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        #self.helper.layout[0] = Div('fecha')
        self.helper[0:4].wrap_together(Column, css_class="form-row")

        # You can dynamically adjust your layout
        self.helper.layout.append(Submit('save', 'save'))
        

    class Meta:
        model = RegistroCatedra
        fields = [
            'clase_teoria',
            'clase_practica',
            'clase_laboratorio',
            'clase_taller']
        # fields = [
        #     'fecha',
        #     'hora_desde',
        #     'hora_hasta',
        #     'catedra',
        #     'docente',
        #     'clase_teoria',
        #     'clase_practica',
        #     'clase_laboratorio',
        #     'clase_taller',
        #     'contenidos_desarrollados',
        #     'contenidos_observacion',
        #     'met_exposicion',
        #     'met_trabajo_ind_grp',
        #     'met_res_ejercicios',
        #     'met_eval',
        #     'met_otros',
        #     'med_pizarra',
        #     'med_video',
        #     'med_pc',
        #     'med_equip',
        #     'med_bibli',
        #     'med_prog',
        #     'med_otros',
        # ]