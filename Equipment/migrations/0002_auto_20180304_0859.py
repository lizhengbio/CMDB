# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Equipment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='token',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=32)),
                ('value', models.CharField(max_length=32)),
                ('register', models.DateTimeField()),
                ('timeout', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='equipment',
            name='Statue',
            field=models.CharField(max_length=32, null=True, verbose_name=b'\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xe7\x8a\xb6\xe6\x80\x81', blank=True),
        ),
    ]
