# Generated by Django 4.1.5 on 2023-01-19 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_message_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='templatelist',
            name='lang',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
