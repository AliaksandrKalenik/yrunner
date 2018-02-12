# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-02-12 16:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('text_style_transfer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StyleTransferRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_created', models.DateTimeField(auto_now_add=True, verbose_name='Record created')),
                ('record_modified', models.DateTimeField(auto_now=True, verbose_name='Record modified')),
                ('text', models.TextField(verbose_name='Input your text')),
                ('status', models.CharField(choices=[('pending', 'pending'), ('in_progress', 'in_progress'), ('completed', 'completed'), ('failed', 'failed')], default='pending', max_length=100)),
                ('result_text', models.TextField(verbose_name='Result text')),
                ('log', models.TextField(default='', verbose_name='Log')),
            ],
        ),
    ]
