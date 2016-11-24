# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0003_auto_20161123_0902'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='encryption',
            field=models.CharField(default=b'aes-128-cfb', max_length=50),
        ),
        migrations.AddField(
            model_name='server',
            name='status',
            field=models.CharField(default=b'Enabled', max_length=20),
        ),
        migrations.AddField(
            model_name='ssuser',
            name='number_server',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='ssuser',
            name='servers_cache',
            field=models.CharField(default=b'', max_length=1024),
        ),
    ]
