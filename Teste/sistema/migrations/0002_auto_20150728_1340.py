# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projeto',
            name='Linguagem',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='projeto',
            name='Link',
            field=models.CharField(unique=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='projeto',
            name='Nome',
            field=models.CharField(unique=True, max_length=100),
        ),
    ]
