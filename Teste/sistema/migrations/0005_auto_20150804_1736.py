# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0004_projeto_atualizado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projeto',
            name='Nome',
            field=models.CharField(max_length=100),
        ),
    ]
