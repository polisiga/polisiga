# Generated by Django 2.2.14 on 2020-10-14 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academico', '0006_auto_20200922_1955'),
    ]

    operations = [
        migrations.RenameField(
            model_name='documento',
            old_name='URL',
            new_name='url',
        ),
        migrations.AlterField(
            model_name='documento',
            name='nro_res',
            field=models.CharField(blank=True, max_length=15),
        ),
    ]
