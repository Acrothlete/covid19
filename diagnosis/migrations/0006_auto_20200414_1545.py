# Generated by Django 3.0.5 on 2020-04-14 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diagnosis', '0005_auto_20200414_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data_base',
            name='state',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='patient_data',
            name='state',
            field=models.CharField(max_length=128),
        ),
    ]
