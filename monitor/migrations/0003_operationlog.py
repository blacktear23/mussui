# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0002_auto_20161127_1129'),
    ]

    operations = [
        migrations.CreateModel(
            name='OperationLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('operator', models.CharField(max_length=255, db_index=True)),
                ('target', models.CharField(max_length=255, db_index=True)),
                ('message', models.TextField(default=b'')),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'operation_log',
            },
        ),
    ]
