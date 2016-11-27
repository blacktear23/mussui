# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConnectionStatistic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('userid', models.IntegerField()),
                ('server_name', models.CharField(max_length=255)),
                ('date', models.DateTimeField()),
                ('connections', models.IntegerField()),
            ],
            options={
                'db_table': 'connection_statistic',
            },
        ),
        migrations.AlterUniqueTogether(
            name='connectionstatistic',
            unique_together=set([('userid', 'date', 'server_name')]),
        ),
    ]
