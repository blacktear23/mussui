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
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hostname', models.CharField(unique=True, max_length=255, db_index=True)),
                ('ip', models.GenericIPAddressField()),
                ('comments', models.TextField(default=b'', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SSUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, db_index=True)),
                ('userid', models.IntegerField(db_index=True)),
                ('password', models.CharField(max_length=255)),
                ('status', models.CharField(default=b'Enabled', max_length=20)),
                ('bandwidth', models.IntegerField(default=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.AlterUniqueTogether(
            name='flowstatistic',
            unique_together=set([('userid', 'date', 'server_name')]),
        ),
    ]
