# Generated by Django 3.2 on 2021-06-01 15:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0005_auto_20210601_1043'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gallery',
            name='background',
        ),
    ]