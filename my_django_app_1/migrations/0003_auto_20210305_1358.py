# Generated by Django 3.1.6 on 2021-03-05 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_django_app_1', '0002_user_pass_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='auto_update',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='id_external',
            field=models.CharField(default='00000000000000000000000000000000022', max_length=36),
        ),
    ]