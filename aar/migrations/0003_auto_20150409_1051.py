# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aar', '0002_auto_20150409_1003'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='child',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='weddingParty',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
