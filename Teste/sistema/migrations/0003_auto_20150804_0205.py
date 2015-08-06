# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0002_auto_20150728_1340'),
    ]

    operations = [
        migrations.AddField(
            model_name='estado',
            name='NumeroMetodos',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='estado',
            name='NumeroTotalLinhas',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='estado',
            name='Projeto',
            field=models.ForeignKey(default=None, to='sistema.Projeto'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='estado',
            name='ComplexidadePorArquivo',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='estado',
            name='ComplexidadePorClasse',
            field=models.DecimalField(default=None, null=True, max_digits=7, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='estado',
            name='ComplexidadePorMetodo',
            field=models.DecimalField(default=None, null=True, max_digits=4, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='estado',
            name='ComplexidadeTotal',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='estado',
            name='Data',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='estado',
            name='Hora',
            field=models.TimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='estado',
            name='NumeroArquivos',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='estado',
            name='NumeroClasses',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='estado',
            name='NumeroLinhasCodigo',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='estado',
            name='NumeroProblemasCriticos',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='estado',
            name='NumeroProblemasModerados',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='estado',
            name='NumeroProblemasMuitoCriticos',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='estado',
            name='NumeroProblemasNormais',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='estado',
            name='NumeroProblemasSimples',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='estado',
            name='NumeroProblemasTotais',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='estado',
            name='ProblemasCriticosPorTamanho',
            field=models.DecimalField(default=None, null=True, max_digits=4, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='estado',
            name='ProblemasModeradosPorTamanho',
            field=models.DecimalField(default=None, null=True, max_digits=4, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='estado',
            name='ProblemasMuitoCriticosPorTamanho',
            field=models.DecimalField(default=None, null=True, max_digits=4, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='estado',
            name='ProblemasNormaisPorTamanho',
            field=models.DecimalField(default=None, null=True, max_digits=4, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='estado',
            name='ProblemasSimplesPorTamanho',
            field=models.DecimalField(default=None, null=True, max_digits=4, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='estado',
            name='TaxaDividaTecnica',
            field=models.DecimalField(default=None, null=True, max_digits=4, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='estado',
            name='TaxaDividaTecnicaPorTamanho',
            field=models.DecimalField(default=None, null=True, max_digits=4, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='estado',
            name='TaxaDuplicacao',
            field=models.DecimalField(default=None, null=True, max_digits=4, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='estado',
            name='TaxaDuplicacaoPorTamanho',
            field=models.DecimalField(default=None, null=True, max_digits=4, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='estado',
            name='TaxaProblemasTotaisPorTamanho',
            field=models.DecimalField(default=None, null=True, max_digits=4, decimal_places=2),
        ),
    ]
