# Generated by Django 2.1 on 2023-06-08 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20230608_0151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageprediction',
            name='output_image',
            field=models.ImageField(default='output_image_default.jpg', upload_to='output_images'),
        ),
    ]
