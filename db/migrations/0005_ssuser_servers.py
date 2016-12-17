# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0004_license'),
    ]

    operations = [
        migrations.AddField(
            model_name='ssuser',
            name='servers',
            field=models.ManyToManyField(to='db.Server'),
        ),
    ]
