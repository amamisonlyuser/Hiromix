# Generated by Django 4.1.5 on 2023-04-11 15:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0015_remove_choice_choice_image_poll_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poll',
            name='image',
        ),
    ]
