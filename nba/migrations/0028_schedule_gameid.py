# Generated by Django 2.0 on 2018-01-09 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0027_auto_20180108_2246'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='gameId',
            field=models.IntegerField(default=0),
        ),
    ]
