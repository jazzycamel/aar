# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aar', '0003_auto_20150409_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='password',
            field=models.CharField(max_length=13, null=True, blank=True),
            preserve_default=True,
        ),
    ]
