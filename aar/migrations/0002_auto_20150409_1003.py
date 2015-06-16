# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aar', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='rsvp',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='attendingDay',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='attendingNight',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
