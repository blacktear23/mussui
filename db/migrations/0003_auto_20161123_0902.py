# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0002_server_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='flowstatistic',
            name='inbound_bandwidth',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='flowstatistic',
            name='outbound_bandwidth',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
