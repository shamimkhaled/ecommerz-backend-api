# Generated by Django 5.0.6 on 2024-06-03 05:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userprofile_last_login'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='last_login',
        ),
    ]
