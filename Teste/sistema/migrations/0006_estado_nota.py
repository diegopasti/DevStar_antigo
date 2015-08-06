# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0005_auto_20150804_1736'),
    ]

    operations = [
        migrations.AddField(
            model_name='estado',
            name='Nota',
            field=models.DecimalField(default=None, max_digits=5,decimal_places=2, null=True),
        ),
    ]
