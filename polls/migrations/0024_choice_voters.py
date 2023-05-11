# Generated by Django 4.1.5 on 2023-04-19 06:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0023_delete_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='voters',
            field=models.ManyToManyField(through='polls.Vote', to=settings.AUTH_USER_MODEL),
        ),
    ]