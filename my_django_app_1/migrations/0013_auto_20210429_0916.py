# Generated by Django 3.1.6 on 2021-04-29 06:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_django_app_1', '0012_auto_20210419_1704'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='documents_list',
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='customers', to=settings.AUTH_USER_MODEL),
        ),
    ]
