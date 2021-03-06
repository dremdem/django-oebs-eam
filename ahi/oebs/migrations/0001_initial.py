# Generated by Django 2.2.1 on 2019-05-06 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AssetHierarchy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset_number', models.CharField(max_length=200, verbose_name='Asset number')),
                ('serial_number', models.CharField(max_length=200, verbose_name='Serial number')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='Description')),
                ('level', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('text_value', models.CharField(blank=True, max_length=500, null=True)),
                ('date_value', models.DateField(blank=True, null=True)),
                ('number_value', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
