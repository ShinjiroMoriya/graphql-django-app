# Generated by Django 2.0.6 on 2018-06-15 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
