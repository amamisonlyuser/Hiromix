# Generated by Django 4.1.5 on 2023-04-20 05:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0032_choice_votes_choice_winner_alter_choice_choice_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='votes',
        ),
        migrations.RemoveField(
            model_name='choice',
            name='winner',
        ),
    ]
