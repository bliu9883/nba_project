# Generated by Django 2.0 on 2017-12-26 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0005_player'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='player_name',
        ),
        migrations.AddField(
            model_name='player',
            name='first_name',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='player',
            name='last_name',
            field=models.CharField(default='', max_length=200),
        ),
    ]
