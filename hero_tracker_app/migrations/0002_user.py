# Generated by Django 3.0.8 on 2020-07-30 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hero_tracker_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('alias', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('pwd_hsh', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
