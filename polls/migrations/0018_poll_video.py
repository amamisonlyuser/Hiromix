# Generated by Django 4.1.5 on 2023-04-11 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0017_poll_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='poll_videos'),
        ),
    ]
