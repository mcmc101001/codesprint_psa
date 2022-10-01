# Generated by Django 4.1.1 on 2022-10-01 10:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_follow_follower_remove_follow_following_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='follower',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='follow', to='main.customuser'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='following',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='followed_by', to='main.customuser'),
        ),
    ]
