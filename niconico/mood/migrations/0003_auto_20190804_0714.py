# Generated by Django 2.2.3 on 2019-08-03 22:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mood', '0002_auto_20190804_0706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mood',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]