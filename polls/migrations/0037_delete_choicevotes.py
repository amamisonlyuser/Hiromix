# Generated by Django 4.1.5 on 2023-04-20 06:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0036_remove_choicevotes_poll_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='choicevotes',
        ),
    ]
