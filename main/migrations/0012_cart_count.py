# Generated by Django 4.1.1 on 2022-10-02 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_remove_cart_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]
