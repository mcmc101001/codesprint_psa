# Generated by Django 4.1.1 on 2022-10-01 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_cart_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
