# Generated by Django 3.1 on 2021-04-27 08:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImgInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=4)),
                ('path', models.CharField(max_length=32)),
                ('time', models.DateField(blank=True, default=datetime.datetime(2021, 4, 27, 16, 24, 54, 927380), null=True)),
                ('file_name', models.CharField(max_length=64)),
            ],
            options={
                'verbose_name': 'imgInfo',
                'db_table': 'ImgInfo',
            },
        ),
        migrations.CreateModel(
            name='MachineOneInfo',
            fields=[
                ('no', models.IntegerField()),
                ('time', models.DateTimeField(primary_key=True, serialize=False)),
                ('id', models.CharField(max_length=8)),
                ('name', models.CharField(max_length=32)),
                ('value', models.JSONField(default=dict)),
            ],
            options={
                'verbose_name': 'machineOneInfo',
                'db_table': 'MachineOneInfo',
            },
        ),
        migrations.CreateModel(
            name='StaticInfo',
            fields=[
                ('id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('no', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=32)),
                ('data', models.DateField()),
            ],
            options={
                'verbose_name': 'staticInfo',
                'db_table': 'StaticInfo',
            },
        ),
    ]