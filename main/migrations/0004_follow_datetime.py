# Generated by Django 4.1.1 on 2022-10-01 10:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_follow'),
    ]

    operations = [
        migrations.AddField(
            model_name='follow',
            name='datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
