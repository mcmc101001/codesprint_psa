# Generated by Django 4.1.1 on 2022-10-01 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_reward'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.ManyToManyField(related_name='follow', to='main.customuser')),
                ('following', models.ManyToManyField(related_name='followed_by', to='main.customuser')),
            ],
        ),
    ]