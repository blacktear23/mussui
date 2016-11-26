# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FlowStatistic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('userid', models.IntegerField()),
                ('server_name', models.CharField(max_length=255)),
                ('inbound_flow', models.IntegerField()),
                ('outbound_flow', models.IntegerField()),
                ('inbound_bandwidth', models.IntegerField()),
                ('outbound_bandwidth', models.IntegerField()),
                ('date', models.DateTimeField()),
            ],
            options={
                'db_table': 'flow_statistic',
            },
        ),
        migrations.AlterUniqueTogether(
            name='flowstatistic',
            unique_together=set([('userid', 'date', 'server_name')]),
        ),
    ]
