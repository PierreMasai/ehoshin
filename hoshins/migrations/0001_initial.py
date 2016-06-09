# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import hoshins.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('type', models.CharField(max_length=2, choices=[('MO', 'Modification'), ('AD', 'Addition'), ('RE', 'Removal'), ('NO', 'Normal')], default='NO')),
                ('text', models.CharField(max_length=1000)),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='Help',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('type', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Hoshin',
            fields=[
                ('name', models.CharField(max_length=200)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('color', models.CharField(max_length=7, validators=[hoshins.models.validate_css_color_code])),
                ('nb_comments', models.IntegerField(default=0)),
                ('nb_items', models.IntegerField(default=0)),
                ('nb_implementation_priorities', models.IntegerField(default=0)),
                ('nb_participants', models.IntegerField(default=0)),
                ('nb_users', models.IntegerField(default=0)),
                ('nb_commentators', models.IntegerField(default=0)),
                ('nb_chatty_commentators', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ImplementationPriority',
            fields=[
                ('name', models.CharField(max_length=200)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('target', models.CharField(max_length=2000)),
                ('leader', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('name', models.CharField(max_length=200)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('target', models.CharField(max_length=2000)),
                ('leader', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Object',
            fields=[
                ('global_id', models.AutoField(serialize=False, primary_key=True)),
                ('owner_temp', models.CharField(max_length=2000, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=256)),
                ('color', models.CharField(max_length=7, default='#81b9c3', validators=[hoshins.models.validate_css_color_code])),
            ],
        ),
        migrations.CreateModel(
            name='Referenceship',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('index', models.CharField(max_length=50, default='', blank=True)),
                ('object', models.ForeignKey(to='hoshins.Object', null=True)),
                ('reference', models.ForeignKey(to='hoshins.Reference')),
            ],
        ),
    ]
