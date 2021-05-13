# Generated by Django 3.1 on 2021-04-28 05:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0003_auto_20210428_1303'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MachineOneInfo',
            new_name='MachineInfo',
        ),
        migrations.AlterModelOptions(
            name='machineinfo',
            options={'verbose_name': 'machineInfo'},
        ),
        migrations.AlterField(
            model_name='imginfo',
            name='time',
            field=models.DateField(blank=True, default=datetime.datetime(2021, 4, 28, 13, 7, 3, 467744), null=True),
        ),
        migrations.AlterModelTable(
            name='machineinfo',
            table='MachineInfo',
        ),
    ]
