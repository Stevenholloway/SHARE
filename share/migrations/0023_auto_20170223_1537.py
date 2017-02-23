# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-23 15:37
from __future__ import unicode_literals

import db.deletion
from django.conf import settings
import django.contrib.postgres.fields.jsonb
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import share.models.ingest


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0022_system_superuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='Harvester',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.TextField(unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='HarvestLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.UUIDField(null=True)),
                ('status', models.IntegerField(choices=[(0, 'Enqueued'), (1, 'In Progress'), (2, 'Failed'), (2, 'Succeeded'), (2, 'Rescheduled')], db_index=True, default=0)),
                ('error', models.TextField(blank=True)),
                ('completions', models.IntegerField(default=0)),
                ('end_date', models.DateTimeField()),
                ('start_date', models.DateTimeField()),
                ('date_started', models.DateTimeField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('share_version', models.TextField(default='2.4.0-39-g81fc8ed0')),
                ('harvester_version', models.TextField()),
                ('source_config_version', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='RawDatum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datum', models.TextField()),
                ('sha256', models.TextField(validators=[django.core.validators.MaxLengthValidator(64)])),
                ('created', models.NullBooleanField(default=False)),
                ('logs', models.ManyToManyField(related_name='raw_data', to='share.HarvestLog')),
            ],
            options={
                'verbose_name_plural': 'Raw Data',
            },
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(unique=True)),
                ('long_title', models.TextField(unique=True)),
                ('home_page', models.URLField(null=True)),
                ('icon', models.ImageField(null=True, storage=share.models.ingest.SourceIconStorage(), upload_to=share.models.ingest.icon_name)),
            ],
        ),
        migrations.CreateModel(
            name='SourceConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.TextField(unique=True)),
                ('version', models.TextField(default='000.000.000')),
                ('base_url', models.URLField()),
                ('earliest_date', models.DateField(null=True)),
                ('rate_limit_allowance', models.PositiveIntegerField(default=5)),
                ('rate_limit_period', models.PositiveIntegerField(default=1)),
                ('harvester_kwargs', django.contrib.postgres.fields.jsonb.JSONField(null=True)),
                ('transformer_kwargs', django.contrib.postgres.fields.jsonb.JSONField(null=True)),
                ('disabled', models.BooleanField(default=False)),
                ('harvester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='share.Harvester')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='share.Source')),
            ],
        ),
        migrations.CreateModel(
            name='SourceIcon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.BinaryField()),
                ('source', models.OneToOneField(on_delete=db.deletion.DatabaseOnDelete(clause='CASCADE'), to='share.Source')),
            ],
        ),
        migrations.CreateModel(
            name='SourceUniqueIdentifier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.TextField()),
                ('source_config', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='share.SourceConfig')),
            ],
        ),
        migrations.CreateModel(
            name='Transformer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.TextField(unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='rawdata',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='rawdata',
            name='source',
        ),
        migrations.RemoveField(
            model_name='rawdata',
            name='tasks',
        ),
        migrations.RemoveField(
            model_name='shareuser',
            name='favicon',
        ),
        migrations.RemoveField(
            model_name='shareuser',
            name='home_page',
        ),
        migrations.RemoveField(
            model_name='shareuser',
            name='long_title',
        ),
        migrations.AlterField(
            model_name='normalizeddata',
            name='raw',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='share.RawDatum'),
        ),
        migrations.DeleteModel(
            name='RawData',
        ),
        migrations.AddField(
            model_name='sourceconfig',
            name='transformer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='share.Transformer'),
        ),
        migrations.AddField(
            model_name='source',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rawdatum',
            name='suid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='share.SourceUniqueIdentifier'),
        ),
        migrations.AddField(
            model_name='harvestlog',
            name='source_config',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='share.SourceConfig'),
        ),
        migrations.AlterUniqueTogether(
            name='sourceuniqueidentifier',
            unique_together=set([('identifier', 'source_config')]),
        ),
        migrations.AlterUniqueTogether(
            name='rawdatum',
            unique_together=set([('suid', 'sha256')]),
        ),
        migrations.AlterUniqueTogether(
            name='harvestlog',
            unique_together=set([('source_config', 'start_date', 'end_date', 'harvester_version', 'source_config_version')]),
        ),
    ]