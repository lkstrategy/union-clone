# Generated by Django 2.2.17 on 2020-12-31 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_companylead_alexarank'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsArticles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=1000)),
                ('url', models.TextField(max_length=1000)),
                ('description', models.TextField(max_length=1500)),
                ('datePublished', models.CharField(max_length=255)),
                ('provider', models.CharField(max_length=255)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.CompanyLead')),
            ],
        ),
    ]
