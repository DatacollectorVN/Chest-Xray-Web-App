# Generated by Django 2.1 on 2023-06-01 10:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import users.image_save_utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ConditionPrediction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.TextField(blank=True, default=None, null=True)),
                ('input_url', models.URLField(blank=True, default=None, null=True)),
                ('output_url', models.URLField(blank=True, default=None, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('date_key', models.IntegerField(blank=True, default=None, null=True)),
                ('result', models.TextField(blank=True, default=None, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_condition_prediction',
            },
        ),
        migrations.CreateModel(
            name='DummyModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.TextField(blank=True, default=None, null=True)),
                ('input_url', models.URLField(blank=True, default=None, null=True)),
                ('output_url', models.URLField(blank=True, default=None, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('date_key', models.IntegerField(blank=True, default=None, null=True)),
                ('result', models.TextField(blank=True, default=None, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(default='default.jpg', upload_to=users.image_save_utils.user_profile_directory_path)),
                ('bio', models.TextField()),
                ('bio2', models.TextField(blank=True, default=None, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
