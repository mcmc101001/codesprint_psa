# Generated by Django 4.1.1 on 2022-10-01 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='follow',
            old_name='from_follow',
            new_name='follower',
        ),
        migrations.RenameField(
            model_name='follow',
            old_name='to_follow',
            new_name='following',
        ),
        migrations.RenameField(
            model_name='request',
            old_name='to_request',
            new_name='requested',
        ),
        migrations.RenameField(
            model_name='request',
            old_name='from_request',
            new_name='requestor',
        ),
    ]
