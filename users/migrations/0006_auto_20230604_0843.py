# Generated by Django 2.1 on 2023-06-04 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20230604_0634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dummymodel',
            name='x_image',
            field=models.ImageField(default='default.jpg', upload_to=''),
        ),
    ]
