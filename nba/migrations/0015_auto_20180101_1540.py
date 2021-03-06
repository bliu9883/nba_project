# Generated by Django 2.0 on 2018-01-01 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0014_auto_20171229_2338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='assists',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='player',
            name='first_name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='player',
            name='last_name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='player',
            name='points',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='player',
            name='rebounds',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='team',
            name='color',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='team',
            name='conference',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='team',
            name='division',
            field=models.CharField(max_length=10),
        ),
    ]
