# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0003_auto_20150804_0205'),
    ]

    operations = [
        migrations.AddField(
            model_name='projeto',
            name='Atualizado',
            field=models.BooleanField(default=False),
        ),
    ]
