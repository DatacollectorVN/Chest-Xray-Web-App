# Generated by Django 2.1 on 2023-06-02 02:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20230602_0218'),
    ]

    operations = [
        migrations.RenameField(
            model_name='conditionprediction',
            old_name='input_url',
            new_name='input_image',
        ),
        migrations.RenameField(
            model_name='conditionprediction',
            old_name='output_url',
            new_name='output_image',
        ),
    ]
