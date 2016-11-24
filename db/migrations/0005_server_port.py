# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0004_auto_20161124_1122'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='port',
            field=models.IntegerField(default=8387),
        ),
    ]
