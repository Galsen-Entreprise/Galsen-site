# Generated by Django 5.0.1 on 2024-10-15 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('galsen', '0026_alter_commande_commande_alter_commande_precision'),
    ]

    operations = [
        migrations.CreateModel(
            name='Traffic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('visits', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('electronics', 'Électronique'), ('fashion', 'Mode et Vêtements'), ('home_garden', 'Maison et Jardin'), ('beauty_health', 'Beauté et Santé'), ('food_drink', 'Alimentation et Boissons'), ('sports_leisure', 'Sport et Loisirs'), ('books_media', 'Livres et Médias'), ('toys_kids', 'Jouets et Enfants'), ('automotive_tools', 'Automobile et Outils'), ('pets', 'Animaux'), ('services', 'Services et Abonnements'), ('special_offers', 'Offres spéciales / Promotions')], default='electronics', max_length=50),
        ),
    ]
