# Generated by Django 2.0 on 2018-01-02 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0015_auto_20180101_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='logo',
            field=models.ImageField(null=True, upload_to='static/logos'),
        ),
        migrations.AddField(
            model_name='team',
            name='url',
            field=models.CharField(default='', max_length=500),
        ),
    ]
