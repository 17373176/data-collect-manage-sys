# Generated by Django 3.1 on 2021-04-29 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0006_auto_20210429_2328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machineinfo',
            name='update_time',
            field=models.DateTimeField(blank=True, primary_key=True, serialize=False),
        ),
    ]
