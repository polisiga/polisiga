# Paquetes que son usados

## django-adminlte3

Paquete que integra la plantilla AdminLTE mediante plantillas base para django.

https://github.com/d-demirci/django-adminlte3
https://github.com/ColorlibHQ/AdminLTE



# Comandos Utiles

## Generar la carpeta venv con el entorno virtual

Primero ubicarse en la raiz del proyecto que es donde se encuentra el archivo
manage.py

python3 -m venv venv

pip install --upgrade pip
pip install -r requirements.txt

## Comando para iniciar el servidor

python manage.py runserver

## Comando para generar datos iniciales y de prueba

python manage.py dumpdata --indent 2 auth -o dumpdata/django_content_type.json
python manage.py dumpdata --indent 2 auth -o dumpdata/auth.json

python manage.py dumpdata --indent 2 academico.alumno -o dumpdata/alumno.json
python manage.py dumpdata --indent 2 academico.periodo -o dumpdata/periodo.json

## Para cargar datos iniciales 




cat .\dumpdata\departamento.json | python .\manage.py loaddata --format=json  -
cat .\dumpdata\carrera.json | python .\manage.py loaddata --format=json  -
cat .\dumpdata\grupohomologas.json | python .\manage.py loaddata --format=json  -
cat .\dumpdata\asignatura.json | python .\manage.py loaddata --format=json  -
cat .\dumpdata\alumno.json | python .\manage.py loaddata --format=json  -
cat .\dumpdata\periodo.json | python .\manage.py loaddata --format=json  -
