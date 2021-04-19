# Generated by Django 3.1.6 on 2021-04-19 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_django_app_1', '0008_auto_20210419_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='localsettings',
            name='record_type',
            field=models.CharField(choices=[('1c_server', '1c server'), ('1c_path', '1c path'), ('1c_user', '1c user'), ('1c_password', '1c user password')], max_length=20),
        ),
        migrations.DeleteModel(
            name='LocalRecordType',
        ),
    ]