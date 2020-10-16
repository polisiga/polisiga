"""Modelos del sistema academico"""
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import m2m_changed
from django.urls import reverse

import datetime


User = settings.AUTH_USER_MODEL


class Alumno(models.Model):
    """Alumno"""
    user = models.OneToOneField(
        User, on_delete=models.PROTECT, blank=True, null=True)
    cedula = models.BigIntegerField(unique=True)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    correo = models.EmailField(unique=True, blank=True)

    def __str__(self):
        return self.nombre + " " + self.apellido

    def get_absolute_url(self):
        """Docstring"""
        return reverse('academico:alumno_detail', kwargs={'pk': self.pk})


# TODO: Verificar si dos Asignaturas tienen el mismo codigo, (GrupoHomologas)
class Asignatura(models.Model):
    """Docstring"""
    codigo = models.CharField(max_length=10, null=True, blank=True)
    siglas = models.CharField(null=True, blank=True, max_length=10)
    nombre = models.CharField(max_length=100, null=True)
    carrera = models.ForeignKey('Carrera', on_delete=models.PROTECT, null=True)
    departamento = models.ForeignKey(
        'Departamento', null=True, on_delete=models.PROTECT)
    enfasis = models.ForeignKey(
        'Enfasis', on_delete=models.PROTECT, null=True, blank=True)
    nivel = models.IntegerField(blank=True, null=True)
    semestre = models.IntegerField(blank=True, null=True)
    prerequisito = models.ManyToManyField('self', blank=True)
    grupohomologas = models.ForeignKey(
        'GrupoHomologas', blank=True, on_delete=models.PROTECT, null=True)

    def get_dpto_siglas(self):
        """Docstring"""
        return self.departamento.siglas

    def homologas(self):
        """
        Nos da las asignaturas homologas en esta asignatura
        """
        try:

            homologas_qs = Asignatura.objects.filter(
                grupohomologas=self.grupohomologas)
            x_str = ' / '.join([str(i) for i in homologasQs])
        except:
            homologas_qs = None
            x_str = ""
        return x_str

    def get_absolute_url(self):
        return f"{self.id}/"

    def __str__(self):
        return str(self.pk) + " - " + self.carrera.siglas + " - " + self.nombre


class Carrera(models.Model):
    """Docstring"""
    nombre = models.CharField(max_length=50)
    siglas = models.CharField(max_length=5, blank=True)
    semestres = models.IntegerField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('academico:carrera_detail', kwargs={'pk': self.pk})

    def __str__(self):

        return self.nombre


class Catedra(models.Model):
    """
    La catedra sirve para agrupar las asignatura homologas que
    pueden ser de diferentes carrras y son dictadas en la misma
    aula.
    La catedra tiene que tener por lo menos una asignatura
    """
    SECCION_SET = (
        ('MI', 'MI'),
        ('MJ', 'MJ'),
        ('MK', 'MK'),
        ('ML', 'ML'),
        ('MM', 'MM'),
        ('MN', 'MN'),
        ('TQ', 'TQ'),
        ('TR', 'TR'),
        ('TS', 'TS'),
        ('TT', 'TT'),
        ('TU', 'TU'),
        ('TV', 'TV'),
        ('TW', 'TW'),
        ('NA', 'NA'),
        ('NB', 'NB'),
        ('NC', 'NC'),
        ('ND', 'ND'),
        ('NE', 'NE'),
        ('NF', 'NF'),
        ('NG', 'NG'),
        ('NH', 'NH'),

    )

    descripcion = models.CharField(default="", max_length=50)
    docentes = models.ManyToManyField('Docente')
    asignaturas = models.ManyToManyField('Asignatura')
    periodo = models.ForeignKey('Periodo', on_delete=models.PROTECT)
    seccion = models.CharField(max_length=5, null=True, choices=SECCION_SET)
    fecha_desde = models.DateField(null=True, blank=True)
    fecha_hasta = models.DateField(null=True, blank=True)
    fecha_1par = models.DateField(
        'Fecha Primer Parcial', null=True, blank=True)
    hora_1par = models.TimeField('Hora Primer Parcial', null=True, blank=True)
    fecha_2par = models.DateField(
        'Fecha Segundo Parcial', null=True, blank=True)
    hora_2par = models.TimeField('Hora Segundo Parcial', null=True, blank=True)
    fecha_1final = models.DateField(
        'Fecha Primer Final', null=True, blank=True)
    hora_1final = models.TimeField('Hora Primer Final', null=True, blank=True)
    fecha_2final = models.DateField(
        'Fecha Segundo Final', null=True, blank=True)
    hora_2final = models.TimeField('Hora Segundo Final', null=True, blank=True)
    # duration = models.DurationField(null=True)
    

    class Meta:
        permissions = [
            (
                "view_own_catedra",
                "Puede ver catedras propias"),
        ]

    def nombre(self):
        """
        El nombre de la catedra es el nombre de la primera asignatura,
        o el nombre de la asignatura principal del grupohomologas
        """
        result = ''
        if self.asignaturas.all().count() == 1:
            result = str(self.pk) + ' - ' + \
                     str(self.asignaturas.first().carrera.siglas) + \
                     ':' + str(self.asignaturas.all().first().nombre)
        elif self.asignaturas.all().count() > 1:
            for idx, asignatura in enumerate(self.asignaturas.all()):
                if idx == 0:
                    result = str(self.pk) + ' - ' + \
                             str(asignatura.carrera.siglas) + ':' + \
                             str(asignatura.nombre)
                else:
                    result = result + '\n      - ' + \
                             str(asignatura.carrera.siglas) + \
                             ':' + str(asignatura.nombre)
        return result + ' - ' + self.seccion + ' - ' + str(self.periodo)

    def homologas(self):
        """
        Queryset de asignaturas homologas.
        """
        try:
            grupo_h = self.asignaturas.all().first().grupohomologas.id
            qs = Asignatura.objects.filter(grupohomologas__id=grupo_h)
            
        except:
            qs = Asignatura.objects.none()
        return qs

    def homologas_str(self):
        return '-'.join([str(i) for i in self.homologas()])

    def lista_registros(self):
        '''
        Nos trae una lista de fechas, en un rango, con un registro de catedra
        enlazado si es que existe en esta fecha

        Parametros:
          desde y hasta: 
        '''

    def plan_activo(self):
        """
        El plan activo es el plan con el campo año(year) mas reciente
        """
        try:
            plan_activo = self.asignaturas.all() \
                .first().plan_set.all().order_by('-year').first()
        except:
            plan_activo = None

        return plan_activo

    def get_absolute_url(self):
        return reverse('academico:catedra_detail_view', kwargs={'pk': self.pk})

    def get_plan(self):
        '''
        Si la primera asignatura tiene grupohomologas entonces trae el
        plan de la asignatura_principal del GrupoHomologas
        '''
        return self.asignaturas.first().plan_set.first()

    def __str__(self):
        return self.nombre()


def catedra_asignaturas_changed(sender, *args, **kwargs):
    """Docstring"""
    if kwargs['action'] == 'pre_add':

        #validar asignaturas homologas
        if kwargs['instance'].asignaturas.count() > 1:
            gh = kwargs['instance'].asignaturas.first().grupohomologas.pk
            for pk_new in kwargs['pk_set']:
                if gh != Asignatura.objects.get(pk=pk_new).grupohomologas:
                    raise ValidationError('Asignaturas no homologas.')


m2m_changed.connect(
    catedra_asignaturas_changed,
    sender=Catedra.asignaturas.through)


class Contenido(models.Model):
    """Docstring"""
    plan = models.ForeignKey('Plan', on_delete=models.PROTECT)
    titulo = models.CharField(max_length=100)

    class Meta:
        ordering = ['titulo']

    def __str__(self):
        return self.titulo


class Departamento(models.Model):
    """Docstring"""
    nombre = models.CharField(max_length=50)
    siglas = models.CharField(max_length=10)

    def __str__(self):
        return self.nombre


class Docente(models.Model):
    '''
    registrocatedra_set: Registros de Catedra de este docente
    '''
    user = models.OneToOneField(User, on_delete=models.PROTECT,
                                null=True, blank=True)
    cedula = models.BigIntegerField(unique=True)
    titulo = models.CharField(max_length=10, null=True, blank=True)
    titulo_grado = models.CharField(max_length=10, null=True, blank=True)
    posgrado = models.CharField(max_length=10, null=True, blank=True)
    apellido = models.CharField(max_length=30)
    nombre = models.CharField(max_length=30)
    email = models.EmailField(blank=True, null=True)
    categoria_docente = models.IntegerField(null=True)

    def get_absolute_url(self):
        return reverse('academico:docente_detail', args=[str(self.id)])

    def __str__(self):
        return str(self.id) + ' - ' + self.apellido + ', ' + self.nombre


class Documento(models.Model):

    TIPO_DOCUMENTO_SET = (
        ('ACTA_CD', 'Acta Consejo Directivo'),
        ('ACTA_CSU', 'Acta Consejo Superior Universitario'),
    )

    tipo = models.CharField(max_length=15, choices=TIPO_DOCUMENTO_SET)
    descripcion = models.CharField(max_length=200)
    fecha = models.DateField(blank=True)
    nro_acta = models.IntegerField(blank=True)
    nro_res = models.CharField(blank=True, max_length=15)
    otra_numeracion = models.CharField(blank=True, max_length=15)
    docentes_relacionados = models.ManyToManyField(Docente)
    url = models.URLField(blank=True)

    def get_absolute_url(self):
        return reverse('academico:documento_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '{} - {} - {}'.format(self.fecha, self.get_tipo_display(), self.descripcion)
    

class Enfasis(models.Model):
    """Docstring"""
    nombre = models.CharField(max_length=50)
    siglas = models.CharField(max_length=5)
    carrera = models.ForeignKey(
        'Carrera', on_delete=models.PROTECT)

    def __str__(self):
        return self.siglas + ' - ' + self.nombre + \
            ' (' + self.carrera.siglas + ')'


class GrupoHomologas(models.Model):
    """Docstring"""
    asignatura_primaria = models.ForeignKey(
        Asignatura, null=True, on_delete=models.PROTECT,
        related_name='asignatura_primaria')
    descripcion = models.CharField(max_length=50)


class Horario(models.Model):
    """Docstring"""
    catedra = models.ForeignKey('Catedra', on_delete=models.PROTECT)
    DIA_SET = (
        (1, 'Lunes'),
        (2, 'Martes'),
        (3, 'Miercoles'),
        (4, 'Jueves'),
        (5, 'Viernes'),
        (6, 'Sabado')
    )
    dia = models.IntegerField(choices=DIA_SET)
    fecha = models.DateField(blank=True, null=True)
    hora_desde = models.TimeField()
    hora_hasta = models.TimeField()


class Periodo(models.Model):
    """Docstring"""
    PERIODO_SET = (
        (1, 'Primer'),
        (2, 'Segundo'),
    )
    numero = models.IntegerField(choices=PERIODO_SET)
    year = models.IntegerField('Año')

    p_lec_desde = models.DateField()
    p_lect_hasta = models.DateField()

    par1_desde = models.DateField(blank=True, null=True)
    par1_hasta = models.DateField(blank=True, null=True)
    par2_desde = models.DateField(blank=True, null=True)
    par2_hasta = models.DateField(blank=True, null=True)
    fin1_desde = models.DateField(blank=True, null=True)
    fin1_hasta = models.DateField(blank=True, null=True)
    fin2_desde = models.DateField(blank=True, null=True)
    fin2_hasta = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.numero) + '/' + str(self.year)


class Plan(models.Model):
    """Docstring"""
    asignatura = models.ForeignKey(
        'Asignatura', on_delete=models.PROTECT, null=True)
    year = models.IntegerField('Año', default=0)

    def from_catedra(self, catedra_pk):
        # asignatura = Catedra.objects.get
        plan_pk = Plan.objects.filter(asignatura=9)
        return plan_pk

    class Meta:
        unique_together = ('asignatura', 'year')

    def __str__(self):
        if self.asignatura is None:
            plan = "None"
        else:
            plan = self.asignatura.nombre + " - " + str(self.year)

        return plan


class RegistroCatedra(models.Model):
    """
    Validaciones:
      - Docente, Catedra y fecha no se pueden repetir
    """
    fecha = models.DateField(null=True)
    hora_desde = models.TimeField(null=True)
    hora_hasta = models.TimeField(null=True)
    catedra = models.ForeignKey('Catedra', on_delete=models.PROTECT)
    docente = models.ForeignKey('Docente', on_delete=models.PROTECT)
    clase_teoria = models.BooleanField('Teoria', default=False)
    clase_practica = models.BooleanField('Practica', default=False)
    clase_laboratorio = models.BooleanField('Laborat.', default=False)
    clase_taller = models.BooleanField('Taller', default=False)
    contenidos_desarrollados = models.ManyToManyField('Contenido', blank=True)
    contenidos_observacion = models.TextField(
        'Observaciones del contenido', default="", blank=True)
    met_exposicion = models.BooleanField('Exposición', default=False)
    met_trabajo_ind_grp = models.BooleanField(
        "Trabajo individual y/o grupal", default=False)
    met_res_ejercicios = models.BooleanField(
        "Resolucion de ejercicios", default=False)
    met_eval = models.BooleanField("Evaluacion", default=False)
    met_otros = models.TextField(
        "Especificar otros metodos utilizados", null=True, blank=True)
    med_pizarra = models.BooleanField("Pizarra", default=False)
    med_video = models.BooleanField("Video", default=False)
    med_pc = models.BooleanField("PC - Proyector Multimedia", default=False)
    med_equip = models.BooleanField("Equipos de Laboratorio", default=False)
    med_bibli = models.BooleanField("Mat. Bibliograficos", default=False)
    med_prog = models.BooleanField("Programas utilitarios", default=False)
    med_otros = models.TextField(
        "Especificar otros medios auxiliares", default="", blank=True)

    def clean(self):
        #Verificar la cantidad de tiempo entre hora_desde y hora_hasta
        datetime_desde = datetime.datetime(
            self.fecha.year,
            self.fecha.month,
            self.fecha.day,
            self.hora_desde.hour,
            self.hora_desde.minute,
            self.hora_desde.second,
            self.hora_desde.microsecond
        )
        datetime_hasta = datetime.datetime(
            self.fecha.year,
            self.fecha.month,
            self.fecha.day,
            self.hora_hasta.hour,
            self.hora_hasta.minute,
            self.hora_hasta.second,
            self.hora_hasta.microsecond
        )

        time_delta = datetime_hasta - datetime_desde
        time_delta_horas = time_delta.total_seconds()/3600


        if time_delta_horas > settings.POLISIGA_MAX_HORAS_CLASE:
            raise ValidationError('Su Registro de Catedra tiene una duracion de ' \
                + str(time_delta_horas) \
                + ' horas, pero solo puede durar ' \
                + str(settings.POLISIGA_MAX_HORAS_CLASE) \
                + ' horas.')

        if time_delta_horas <= 0:
            raise ValidationError('La duracion del Registro de Catedra debe ser mayor a 0.')

    class Meta:
        """Docstring"""
        constraints = [
            models.UniqueConstraint(
                fields=['fecha', 'catedra', 'docente'],
                name='unique_registrocatedra'
            ),
        ]
        permissions = [
            (
                "view_own_registrocatedra",
                "Puede ver registros de catedra propios"),
            (
                "add_own_registrocatedra",
                "Puede añadir registros de catedra propios"),
        ]

    def plan_activo(self):
        """Docstring"""
        return self.catedra.asignaturas.first() \
                   .plan_set.all().order_by('-year').first()

    def get_absolute_url(self):
        """Docstring"""
        return reverse('academico:registro-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.id)


