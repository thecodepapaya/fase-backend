# Generated by Django 3.1.6 on 2021-03-13 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faculty', '0007_auto_20210311_2242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faculty',
            name='google_uid',
            field=models.CharField(max_length=28),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]