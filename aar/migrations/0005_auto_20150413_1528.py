# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('aar', '0004_invitation_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MealOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=512)),
                ('course', models.CharField(blank=True, max_length=20, null=True, choices=[(b'starter', b'starter'), (b'main', b'main'), (b'dessert', b'dessert')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('shortName', models.CharField(max_length=3)),
                ('topTable', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TablePosition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.IntegerField(validators=(django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)))),
                ('table', models.ForeignKey(related_name=b'position', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='aar.Table', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='tableposition',
            unique_together=set([('table', 'position')]),
        ),
        migrations.AddField(
            model_name='meal',
            name='dessert',
            field=models.ForeignKey(related_name=b'dessert', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='aar.MealOption', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='meal',
            name='main',
            field=models.ForeignKey(related_name=b'main', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='aar.MealOption', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='meal',
            name='starter',
            field=models.ForeignKey(related_name=b'starter', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='aar.MealOption', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='meal',
            field=models.OneToOneField(related_name=b'person', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='aar.Meal'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='tablePosition',
            field=models.OneToOneField(related_name=b'person', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='aar.TablePosition'),
            preserve_default=True,
        ),
    ]
