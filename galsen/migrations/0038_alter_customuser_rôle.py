# Generated by Django 5.0.1 on 2024-11-27 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('galsen', '0037_alter_customuser_situation_matrimoniale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='rôle',
            field=models.CharField(choices=[('professionnel', 'Professionnel(le)'), ('ecole', 'Ecole'), ('entreprise', 'Entreprise')], default='personnel', max_length=255),
        ),
    ]
