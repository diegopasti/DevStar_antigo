# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0006_estado_nota'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estado',
            name='Hora',
        ),
        migrations.AddField(
            model_name='estado',
            name='ProjetoUsuario',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='estado',
            name='Data',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
