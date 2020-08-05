from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, Field, Column, HTML

from tempus_dominus.widgets import DatePicker

from .models import ( 
    Asignatura,
    Catedra,
    Contenido,
    RegistroCatedra,
)

class MultiSelect2Widget(forms.ModelMultipleChoiceField):
    class Media:
        js = ('admin-lte/plugins/select2/js/select2.full.min.js')

class FechaWidget(forms.widgets.TextInput):
    class Media:
        js = (
            'admin-lte/plugins/tempusdominus-bootstrap-4/js/tempusdominus-bootstrap-4.min.js',
            'admin-lte/plugins/moment/moment-with-locales.min.js',)

    template_name = 'widgets/fecha.html'

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
        

    class Meta:
        model = RegistroCatedra
        fields = [
            'fecha',
            'hora_desde',
            'hora_hasta',
            'catedra',
            'docente',
            'clase_teoria',
            'clase_practica',
            'clase_laboratorio',
            'clase_taller',
            'contenidos_desarrollados',
            'contenidos_observacion',
            'met_exposicion',
            'met_trabajo_ind_grp',
            'met_res_ejercicios',
            'met_eval',
            'met_otros',
            'med_pizarra',
            'med_video',
            'med_pc',
            'med_equip',
            'med_bibli',
            'med_prog',
            'med_otros',
        ]
        widgets = {
            'fecha': FechaWidget(),
        }
class RegistroCatedraFormCrispy(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RegistroCatedraForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        #self.helper.layout[0] = Div('fecha')
        self.helper[0:3].wrap_together(Div, css_class="form-row")
        self.helper[0].wrap(Div, css_class="card-body")
        self.helper[0].wrap(Div, css_class="card")
        self.helper.layout[0].insert(0, Div(css_class="card-header"))
        self.helper.layout[0][0].insert(0, HTML('<h3 class="card-title">Detalles</h3>'))

        self.helper[1:5].wrap_together(Div, css_class="form-row")
        self.helper[1].wrap(Div, css_class="card-body")
        self.helper[1].wrap(Div, css_class="card")
        self.helper.layout[1].insert(0, Div(css_class="card-header"))
        self.helper.layout[1][0].insert(0, HTML('<h3 class="card-title">Detalles</h3>'))


        #self.helper.filter("custom-control custom-checkbox").update_attributes(css_class="ml-3")

        # You can dynamically adjust your layout
        self.helper.layout.append(Submit('save', 'save'))
        

    class Meta:
        model = RegistroCatedra
        fields = [
            'fecha',
            'hora_desde',
            'hora_hasta',
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