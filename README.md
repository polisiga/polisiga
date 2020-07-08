# Paquetes que son usados

## django-adminlte3

Paquete que integra la plantilla AdminLTE mediante plantillas base para django.

https://github.com/d-demirci/django-adminlte3
https://github.com/ColorlibHQ/AdminLTE



# Comandos Utiles

## Como Clonar

git clone git@github.com:DelmisMartinez/polisiga.git 
linea asd as

## Generar la carpeta venv con el entorno virtual

Primero ubicarse en la raiz del proyecto que es donde se encuentra el archivo
manage.py

(para powershell habilitar para ejecutar scripts https://docs.microsoft.com/es-es/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7)

Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unestricted

python -m venv venv

pip install --upgrade pip
pip install -r requirements.txt

## Preparar primer inicio

(para generar las BBDD)
python manage.py migrate

(crear un superusuario)
python manage.py createsuperuser

(cargar datos de prueba)
python .\manage.py loaddata departamento



## Comando para iniciar el servidor

python manage.py runserver

## Comando para generar datos iniciales y de prueba

python manage.py dumpdata --indent 2 academico.departamento -o dumpdata/departamento.json
python manage.py dumpdata --indent 2 academico.alumno -o dumpdata/alumno.json
