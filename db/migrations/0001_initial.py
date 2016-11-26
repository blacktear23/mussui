# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hostname', models.CharField(unique=True, max_length=255, db_index=True)),
                ('ip', models.GenericIPAddressField()),
                ('port', models.IntegerField(default=8387)),
                ('status', models.CharField(default=b'Enabled', max_length=20)),
                ('encryption', models.CharField(default=b'aes-128-cfb', max_length=50)),
                ('comments', models.TextField(default=b'', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
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
                ('servers_cache', models.CharField(default=b'', max_length=1024)),
                ('number_server', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]
