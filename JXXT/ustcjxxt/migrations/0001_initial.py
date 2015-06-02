# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assistant',
            fields=[
                ('astId', models.CharField(max_length=30, serialize=False, primary_key=True)),
                ('password', models.CharField(max_length=60)),
                ('beginTime', models.DateField()),
                ('endTime', models.DateField()),
                ('comment', models.TextField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('studentId', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('password', models.CharField(max_length=60)),
                ('name', models.CharField(max_length=30)),
                ('age', models.IntegerField(blank=True)),
                ('sex', models.CharField(max_length=1, choices=[(b'm', b'\xe7\x94\xb7'), (b'f', b'\xe5\xa5\xb3')])),
                ('address', models.CharField(max_length=60, blank=True)),
                ('email', models.EmailField(max_length=254)),
                ('headshot', models.ImageField(upload_to=b'stuPic/', blank=True)),
            ],
            options={
                'ordering': ['studentId'],
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('teacherId', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('password', models.CharField(max_length=60)),
                ('name', models.CharField(max_length=30)),
                ('age', models.IntegerField(blank=True)),
                ('sex', models.CharField(max_length=1, choices=[(b'm', b'\xe7\x94\xb7'), (b'f', b'\xe5\xa5\xb3')])),
                ('address', models.CharField(max_length=60, blank=True)),
                ('email', models.EmailField(max_length=254)),
                ('headshot', models.ImageField(upload_to=b'stuPic/', blank=True)),
            ],
            options={
                'ordering': ['teacherId'],
            },
        ),
        migrations.AddField(
            model_name='assistant',
            name='assitant',
            field=models.ForeignKey(to='ustcjxxt.Student'),
        ),
        migrations.AddField(
            model_name='assistant',
            name='teacher',
            field=models.ManyToManyField(to='ustcjxxt.Teacher'),
        ),
    ]
