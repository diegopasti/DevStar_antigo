# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0007_auto_20150805_2130'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estado',
            name='ProjetoUsuario',
        ),
        migrations.AddField(
            model_name='projeto',
            name='ProjetoUsuario',
            field=models.BooleanField(default=False),
        ),
    ]
