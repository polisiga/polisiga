from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone


User = settings.AUTH_USER_MODEL


class Alumno(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.PROTECT,blank=True, null=True)
    cedula = models.BigIntegerField(unique=True)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    correo = models.EmailField(unique=True,blank=True)
    
    def __str__(self):
        return self.nombre + " "  + self.apellido
        
    def get_absolute_url(self):
        return reverse('academico:alumno_detail', kwargs={'pk': self.pk})

# TODO: Verificar si dos Asignaturas tienen el mismo codigo, (GrupoHomologas)
class Asignatura(models.Model):
    codigo = models.CharField(max_length=10, null=True, blank=True)
    siglas = models.CharField(null=True, max_length=10)
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
        return self.departamento.siglas

    def homologas(self):
        """
        Nos da las asignaturas homologas en esta asignatura
        """
        try:

            o = Asignatura.objects.filter(grupohomologas=self.grupohomologas)
            x_str = ' / '.join([str(i) for i in o])
        except:
            o = None
            x_str = ""
        return x_str

    def __str__(self):
        return str(self.pk) + " - " + self.carrera.siglas + " - " + self.nombre


class Carrera(models.Model):
    nombre = models.CharField(max_length=50)
    siglas = models.CharField(max_length=5, blank=True)
    semestres = models.IntegerField(blank=True, null=True)

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
    #duration = models.DurationField(null=True)

    def nombre(self):
        """
        El nombre de la catedra es el nombre de la primera asignatura
        """
        try:
            result = str(self.asignaturas.all().first()) + \
                ' - ' + self.seccion + ' - ' + str(self.periodo)
        except:
            result = 'sin nombre'
        return result

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

    def plan_activo(self):
        """
        El plan activo es el plan con el campo año(year) mas reciente
        """
        try:
            o = self.asignaturas.all().first().plan_set.all().order_by('-year').first()
        except:
            o = None

        return o

    # def clean(self):
    #     try:
    #         grupo_h = self.asignaturas.all().first().grupohomologas.id

    #         asig_count = self.asignaturas.all().count()
    #         asig_h = self.asignaturas.all().filter(grupohomologas__id=grupo_h).count()

    #     except:
    #         asig_h, asig_count = 0
    #     if not asig_count == asig_h:
    #         raise ValidationError(
    #             'Todas las asignaturas deben estar en el mismo grupo de homologas.')

    def save(self, *args, **kwargs):
        # self.slug = slugify(self.headline)
        print("saving Catedra")

        super(Catedra, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('academico:catedra-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.nombre()


class Contenido(models.Model):
    plan = models.ForeignKey('Plan', on_delete=models.PROTECT)
    titulo = models.CharField(max_length=100)

    def __str__(self):
        return self.titulo


class Departamento(models.Model):
    nombre = models.CharField(max_length=50)
    siglas = models.CharField(max_length=10)

    def __str__(self):
        return self.nombre


class Docente(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, null=True)
    cedula = models.BigIntegerField(unique=True)
    titulo = models.CharField(max_length=10)
    titulo_grado = models.CharField(max_length=10)
    posgrado = models.CharField(max_length=10, null=True, blank=True)
    apellido = models.CharField(max_length=30)
    nombre = models.CharField(max_length=30)
    categoria_docente = models.IntegerField(null=True)

    def registros(self):
        return RegistroCatedra.object.all().filter(docente__id=self.id)

    def __str__(self):
        return str(self.id) + ' - ' + self.apellido + ', ' + self.nombre


class Enfasis(models.Model):
    nombre = models.CharField(max_length=50)
    siglas = models.CharField(max_length=5)
    carrera = models.ForeignKey(
        'Carrera', on_delete=models.PROTECT)

    def __str__(self):
        return self.siglas + ' - ' + self.nombre + \
            ' (' + self.carrera.siglas + ')'


class GrupoHomologas(models.Model):
    descripcion = models.CharField(max_length=50)


class Horario(models.Model):
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
    asignatura = models.ForeignKey(
        'Asignatura', on_delete=models.PROTECT, null=True)
    year = models.IntegerField('Año', default=0)

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
    sdkas
    """
    fecha = models.DateField(null=True)
    hora_desde = models.TimeField(null=True)
    hora_hasta = models.TimeField(null=True)
    catedra = models.ForeignKey('Catedra', on_delete=models.PROTECT, null=True)
    docente = models.ForeignKey('Docente', on_delete=models.PROTECT, null=True)
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
    met_otros = models.TextField("Otros metodos", null=True, blank=True)
    med_pizarra = models.BooleanField("Pizarra", default=False)
    med_video = models.BooleanField("Video", default=False)
    med_pc = models.BooleanField("PC - Proyector Multimedia", default=False)
    med_equip = models.BooleanField("Equipos de Laboratorio", default=False)
    med_bibli = models.BooleanField("Mat. Bibliograficos", default=False)
    med_prog = models.BooleanField("Programas utilitarios", default=False)
    med_otros = models.TextField(
        "Especificar otros medios auxiliares", default="", blank=True)

    def get_absolute_url(self):

        return reverse('academico:registro-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.id)
