# Generated by Django 4.1.5 on 2023-04-08 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0013_remove_poll_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='image',
        ),
        migrations.AddField(
            model_name='choice',
            name='choice_image',
            field=models.ImageField(blank=True, null=True, upload_to='choice_images'),
        ),
    ]
