# Generated by Django 2.1 on 2023-06-12 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_diseaseprediction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diseaseprediction',
            name='score',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]