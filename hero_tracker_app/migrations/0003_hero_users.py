# Generated by Django 3.0.8 on 2020-07-30 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hero_tracker_app', '0002_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='hero',
            name='users',
            field=models.ManyToManyField(related_name='heroes', to='hero_tracker_app.User'),
        ),
    ]