# Generated by Django 2.2.17 on 2020-12-23 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20201223_2149'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_client',
            field=models.BooleanField(default=False),
        ),
    ]
