# Generated by Django 4.1.1 on 2022-10-02 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_alter_customuser_birthday'),
    ]

    operations = [
        migrations.AddField(
            model_name='reward',
            name='image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='birthday',
            field=models.DateField(),
        ),
    ]