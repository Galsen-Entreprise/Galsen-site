# Generated by Django 5.0.1 on 2024-11-13 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('galsen', '0031_rename_date_creation_reponse_date_creation_annonce_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='annonce',
            name='prix',
            field=models.DecimalField(decimal_places=2, default=2000, max_digits=10),
            preserve_default=False,
        ),
    ]
