# Generated by Django 5.0.2 on 2024-03-16 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('galsen', '0006_boutique_devise_money'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='firstname',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='lastname',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
