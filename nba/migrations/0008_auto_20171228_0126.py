# Generated by Django 2.0 on 2017-12-28 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0007_team_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='conference',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='team',
            name='division',
            field=models.CharField(default='', max_length=10),
        ),
    ]