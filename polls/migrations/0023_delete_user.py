# Generated by Django 4.1.5 on 2023-04-19 06:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0022_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]