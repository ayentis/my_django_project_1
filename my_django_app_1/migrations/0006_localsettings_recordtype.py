# Generated by Django 3.1.6 on 2021-04-19 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_django_app_1', '0005_auto_20210419_1315'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecordType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_type', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='LocalSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=250)),
                ('record_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='my_django_app_1.recordtype')),
            ],
        ),
    ]
