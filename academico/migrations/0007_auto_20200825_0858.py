# Generated by Django 2.2.14 on 2020-08-25 12:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academico', '0006_auto_20200813_0952'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='registrocatedra',
            options={'permissions': [('can_add_own', 'Puede añadir sus Registros de Catedra propios')]},
        ),
    ]