# Generated by Django 2.2.17 on 2021-01-05 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_auto_20201231_1833'),
    ]

    operations = [
        migrations.AddField(
            model_name='leadcomplete',
            name='status',
            field=models.CharField(choices=[('open', 'Open'), ('favorite', 'favorite'), ('archived', 'archived'), ('acccepted', 'accepted')], default='open', max_length=32),
        ),
    ]
