# Generated by Django 5.0.1 on 2024-10-24 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('galsen', '0028_facture'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='access',
            field=models.CharField(choices=[('autorised', 'Autorisé(e)'), ('no_autorised', 'Non autorisé(e)')], default='no_autorised', max_length=255),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='rôle',
            field=models.CharField(choices=[('personnel', 'Personnel(le)'), ('ecole', 'Ecole'), ('entreprise', 'Entreprise')], default='personnel', max_length=255),
        ),
    ]
