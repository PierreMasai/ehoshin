# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('hoshins', '0001_initial'),
        ('teams', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='reference',
            name='team',
            field=models.ForeignKey(related_name='references', to='teams.Team'),
        ),
        migrations.AddField(
            model_name='object',
            name='belongs_to',
            field=models.ForeignKey(related_name='hoshins', to='teams.Team'),
        ),
        migrations.AddField(
            model_name='object',
            name='owner',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='object',
            name='references',
            field=models.ManyToManyField(through='hoshins.Referenceship', blank=True, to='hoshins.Reference', related_name='reference_of'),
        ),
        migrations.AddField(
            model_name='item',
            name='object_ptr',
            field=models.OneToOneField(to='hoshins.Object'),
        ),
        migrations.AddField(
            model_name='item',
            name='parent',
            field=models.ForeignKey(related_name='children', to='hoshins.Hoshin'),
        ),
        migrations.AddField(
            model_name='implementationpriority',
            name='object_ptr',
            field=models.OneToOneField(to='hoshins.Object'),
        ),
        migrations.AddField(
            model_name='implementationpriority',
            name='parent',
            field=models.ForeignKey(related_name='children', to='hoshins.Item'),
        ),
        migrations.AddField(
            model_name='hoshin',
            name='object_ptr',
            field=models.OneToOneField(to='hoshins.Object'),
        ),
        migrations.AddField(
            model_name='help',
            name='user',
            field=models.ForeignKey(related_name='helps', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='object_ptr',
            field=models.ForeignKey(to='hoshins.Object'),
        ),
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(related_name='comments', to='hoshins.Object'),
        ),
    ]
