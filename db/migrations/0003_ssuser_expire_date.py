# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0002_ssuser_login_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='ssuser',
            name='expire_date',
            field=models.DateTimeField(null=True),
        ),
    ]
