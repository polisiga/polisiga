# Generated by Django 2.2.14 on 2020-08-27 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academico', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='docente',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
