# Generated by Django 2.0 on 2017-12-23 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='tri_code',
            field=models.CharField(default=2, max_length=200),
            preserve_default=False,
        ),
    ]
