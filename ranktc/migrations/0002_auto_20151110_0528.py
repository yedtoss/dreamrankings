# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ranktc', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RatingsPicture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(auto_now_add=True, null=True)),
                ('picture_location', models.TextField(null=True, blank=True)),
                ('challenge_type', models.TextField(null=True, blank=True)),
                ('picture_done', models.NullBooleanField()),
            ],
        ),
        migrations.AddField(
            model_name='member',
            name='challenge_type',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='member',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
