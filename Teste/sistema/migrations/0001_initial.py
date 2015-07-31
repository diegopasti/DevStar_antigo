# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Nome', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Data', models.DateField()),
                ('Hora', models.TimeField()),
                ('NumeroLinhasCodigo', models.IntegerField()),
                ('NumeroClasses', models.IntegerField()),
                ('NumeroArquivos', models.IntegerField()),
                ('ComplexidadeTotal', models.DecimalField(max_digits=10, decimal_places=2)),
                ('ComplexidadePorMetodo', models.DecimalField(max_digits=4, decimal_places=2)),
                ('ComplexidadePorClasse', models.DecimalField(max_digits=7, decimal_places=2)),
                ('ComplexidadePorArquivo', models.DecimalField(max_digits=10, decimal_places=2)),
                ('TaxaDuplicacao', models.DecimalField(max_digits=4, decimal_places=2)),
                ('TaxaDuplicacaoPorTamanho', models.DecimalField(max_digits=4, decimal_places=2)),
                ('NumeroProblemasTotais', models.IntegerField()),
                ('TaxaProblemasTotaisPorTamanho', models.DecimalField(max_digits=4, decimal_places=2)),
                ('TaxaDividaTecnica', models.DecimalField(max_digits=4, decimal_places=2)),
                ('TaxaDividaTecnicaPorTamanho', models.DecimalField(max_digits=4, decimal_places=2)),
                ('NumeroProblemasMuitoCriticos', models.IntegerField()),
                ('NumeroProblemasCriticos', models.IntegerField()),
                ('NumeroProblemasModerados', models.IntegerField()),
                ('NumeroProblemasNormais', models.IntegerField()),
                ('NumeroProblemasSimples', models.IntegerField()),
                ('ProblemasMuitoCriticosPorTamanho', models.DecimalField(max_digits=4, decimal_places=2)),
                ('ProblemasCriticosPorTamanho', models.DecimalField(max_digits=4, decimal_places=2)),
                ('ProblemasModeradosPorTamanho', models.DecimalField(max_digits=4, decimal_places=2)),
                ('ProblemasNormaisPorTamanho', models.DecimalField(max_digits=4, decimal_places=2)),
                ('ProblemasSimplesPorTamanho', models.DecimalField(max_digits=4, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='Projeto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Nome', models.CharField(max_length=100)),
                ('Linguagem', models.CharField(max_length=50)),
                ('Link', models.CharField(max_length=100)),
            ],
        ),
    ]
