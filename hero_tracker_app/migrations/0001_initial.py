# Generated by Django 3.0.8 on 2020-07-30 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hero',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('desc', models.TextField()),
                ('movement_type', models.CharField(max_length=255)),
                ('weapon_type', models.CharField(max_length=255)),
                ('color', models.CharField(max_length=255)),
                ('debut_date', models.DateField()),
                ('lv_40_HP', models.IntegerField()),
                ('lv_40_atk', models.IntegerField()),
                ('lv_40_spd', models.IntegerField()),
                ('lv_40_def', models.IntegerField()),
                ('lv_40_res', models.IntegerField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
