# Generated by Django 2.1 on 2023-06-07 08:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20230607_0310'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='imageprediction',
            table='users_image_prediction',
        ),
    ]