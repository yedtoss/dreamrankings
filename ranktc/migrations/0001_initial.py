# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('handle', models.TextField(null=True, blank=True)),
                ('rating', models.IntegerField(default=5)),
                ('volatibility', models.IntegerField(default=5)),
                ('mu', models.DecimalField(default=0, max_digits=19, decimal_places=2)),
                ('sigma', models.DecimalField(default=0, max_digits=19, decimal_places=2)),
            ],
        ),
    ]
