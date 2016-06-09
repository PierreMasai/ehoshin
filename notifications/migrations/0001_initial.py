# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import jsonfield.fields
import notifications.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('level', models.CharField(max_length=20, choices=[('success', 'success'), ('info', 'info'), ('warning', 'warning'), ('error', 'error')], default='info')),
                ('unread', models.BooleanField(default=True)),
                ('actor_object_id', models.CharField(max_length=255)),
                ('verb', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('target_object_id', models.CharField(max_length=255, blank=True, null=True)),
                ('action_object_object_id', models.CharField(max_length=255, blank=True, null=True)),
                ('timestamp', models.DateTimeField(default=notifications.models.now)),
                ('public', models.BooleanField(default=True)),
                ('deleted', models.BooleanField(default=False)),
                ('emailed', models.BooleanField(default=False)),
                ('data', jsonfield.fields.JSONField(blank=True, null=True)),
                ('action_object_content_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', related_name='notify_action_object', null=True)),
                ('actor_content_type', models.ForeignKey(related_name='notify_actor', to='contenttypes.ContentType')),
                ('recipient', models.ForeignKey(related_name='notifications', to=settings.AUTH_USER_MODEL)),
                ('target_content_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', related_name='notify_target', null=True)),
            ],
            options={
                'ordering': ('-timestamp',),
            },
        ),
    ]
