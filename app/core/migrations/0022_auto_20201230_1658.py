# Generated by Django 2.2.17 on 2020-12-30 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='createdAt',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='message',
            name='updatedAt',
            field=models.CharField(max_length=255),
        ),
    ]
