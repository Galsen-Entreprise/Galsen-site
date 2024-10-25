from django.db import models

from django.contrib.auth.models import AbstractUser as BaseAbstractUser, BaseUserManager, Permission, Group
from django.conf import settings
from django.urls import reverse
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        # Votre implémentation pour créer un utilisateur
        pass

    def create_superuser(self, email, username, password=None, **extra_fields):
        # Votre implémentation pour créer un superutilisateur
        pass

class AbstractUser(BaseAbstractUser):
    # Ajoutez ces deux lignes avec related_name
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)


# Create your models here.
class CustomUser(AbstractUser):
    LANGUE = [
        ('français', 'Français'),
        ('anglais', 'Anglais'),
        ('spagnol', 'Espagnol'),
        ('italien', 'Italien'),
        ('arabe', 'Arabe'),
    ]
    ACCESS = [
        ('autorised', 'Autorisé(e)'),
        ('no_autorised', 'Non autorisé(e)'),
    ]
    ROLES = [
        ('personnel', 'Personnel(le)'),
        ('ecole', 'Ecole'),
        ('entreprise', 'Entreprise'),
    ]
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    banner_image = models.ImageField(upload_to='banner_images/', null=True, blank=True)
    GENRE = [
        ('homme', 'Homme'),
        ('femme', 'Femme'),
    ]
    SITUATION_MATRIMONIALE = [
        ('celibataire', 'Célibataire'),
        ('marie', 'Marié(e)'),
        ('fiance', 'Fiancé(e)'),
        ('divorce', 'Divorcé(e)'),
    ]
    marque_dispositif = models.CharField(max_length=255, null=True, blank=True)
    metier = models.CharField(max_length=150, null=True, blank=True)
    etablissement = models.CharField(max_length=255, null=True, blank=True)
    pays = models.CharField(max_length=50, null=True, blank=True)
    ville = models.CharField(max_length=50, null=True, blank=True)
    quartier = models.CharField(max_length=50, null=True, blank=True)
    langue = models.CharField(max_length=255, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    indicatif_pays = models.CharField(max_length=15, null=True, blank=True)
    number_phone = models.CharField(max_length=15, null=True, blank=True)
    number_whatsapp = models.CharField(max_length=15, null=True, blank=True)
    number_telegram = models.CharField(max_length=15, null=True, blank=True)
    instagram_link = models.URLField(null=True, blank=True)
    twitter_link = models.URLField(null=True, blank=True)
    youtube_link = models.URLField(null=True, blank=True)
    website_link = models.URLField(null=True, blank=True)
    langue = models.CharField(max_length=255, choices=LANGUE, default='français')
    rôle = models.CharField(max_length=255, choices=ROLES, default='personnel')
    access = models.CharField(max_length=255, choices=ACCESS, default='no_autorised')
    genre = models.CharField(max_length=255, choices=GENRE, default='homme')
    situation_matrimoniale = models.CharField(max_length=20, choices=SITUATION_MATRIMONIALE, default='celibataire')
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following_users', blank=True)
    
    def get_following(self):
        return self.following_users.all()
    
    def get_following_count(self):
        return self.following_users.count()
    
    def get_followers(self):
        return self.followers.all()

    def get_followers_count(self):
        return self.followers.count()
    
    def is_following(self, user):
        return self.following_users.filter(id=user.id).exists()
    
    def get_absolute_url(self):
        return reverse('a_propos_current_user')
    
    def total_likes_received(self):
        total_likes = 0
        for post in self.post_set.all():
            total_likes += post.like_post.count()
        return total_likes
    
    def __str__(self):
        return self.username

  
class Profil(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    description = models.TextField()
    
    def __str__(self):
        return self.user.username
    
class Experience(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    def __str__(self):
        return self.user.username
    
class Formation(models.Model): # Formation == Filiére
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    def __str__(self):
        return self.user.username
    
class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    video = models.FileField(upload_to='post_videos/')
    contenu_post = models.TextField()
    tag_post = models.CharField(max_length=255)
    session_info = models.CharField(max_length=255, null=True, blank=True)
    date_creation_post = models.DateTimeField(auto_now_add=True)
    like_post = models.ManyToManyField(CustomUser, blank=True, related_name="likes")
    dislike = models.ManyToManyField(CustomUser, blank=True, related_name='dislikes')
    shared_boby = models.TextField(blank=True, null=True)
    share_on = models.DateTimeField(blank=True, null=True)
    shared_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='+')
    
    class Meta:
        ordering = ['-date_creation_post', '-share_on']

    @property
    def nombre_commentaire(self):
        return Commentaire.objects.filter(post=self).count()
    
class MediasPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/')
    
class Commentaire(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    contenu_commentaire = models.TextField()
    image = models.ImageField(upload_to='comment_images/')
    date_creation = models.DateTimeField(auto_now_add=True)
    
    @property
    def nombre_response(self):
        return Reponse.objects.filter(comment=self).count()
    
class Share(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    
class Reponse(models.Model):
    commentaire = models.ForeignKey(Commentaire, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    contenu_text = models.TextField()
    image = models.ImageField(upload_to='response_images/')
    date_creation = models.DateTimeField(auto_now_add=True)
    
class Job(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    contenu_job = models.TextField()
    postule_job = models.ManyToManyField(CustomUser, blank=True, related_name="postule")
    dispostule = models.ManyToManyField(CustomUser, blank=True, related_name='dispostule')
    date_creation_post = models.DateTimeField(auto_now_add=True)
    shared_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='+')
    
    def __str__(self):
        return self.user.username
    
class ShareJob(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    
class Boutique(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    nom_boutique = models.CharField(max_length=255)
    devise_boutique = models.CharField(max_length=255)
    devise_money = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    photo_profil = models.ImageField(upload_to='boutique_profil/')
    banner_image = models.ImageField(upload_to='boutique_banner/')
    date_creation = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.nom_boutique
    
class Client(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    boutique = models.ForeignKey(Boutique, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Électronique'),
        ('fashion', 'Mode et Vêtements'),
        ('home_garden', 'Maison et Jardin'),
        ('beauty_health', 'Beauté et Santé'),
        ('food_drink', 'Alimentation et Boissons'),
        ('sports_leisure', 'Sport et Loisirs'),
        ('books_media', 'Livres et Médias'),
        ('toys_kids', 'Jouets et Enfants'),
        ('automotive_tools', 'Automobile et Outils'),
        ('pets', 'Animaux'),
        ('services', 'Services et Abonnements'),
        ('special_offers', 'Offres spéciales / Promotions'),
    ]
    boutique = models.ForeignKey(Boutique, on_delete=models.CASCADE)
    video = models.FileField(upload_to='product_videos/')
    nom_produit = models.CharField(max_length=255)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    quantite_stock = models.IntegerField(null=True, blank=True)
    fournisseur = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='electronics')
    date_creation = models.DateTimeField(auto_now_add=True)
    
class Facture(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_public = models.BooleanField(default=False) 
    date_creation = models.DateTimeField(auto_now_add=True)

class Commande(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    commande = models.CharField(max_length=255, null=True, blank=True)
    precision = models.TextField(null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    
class ReponseCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    contenu_text = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    
class MediasProduct(models.Model):
    produit = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')

class Notification(models.Model):
    # 1 = Like, 2 = Comment, 3 = Follow
    notification_type = models.IntegerField()
    to_user = models.ForeignKey(CustomUser, related_name='notification_to', on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey(CustomUser, related_name='notification_from', on_delete=models.CASCADE, null=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    comment = models.ForeignKey('Commentaire', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    user_has_seen = models.BooleanField(default=False)
    
class Traffic(models.Model):
    date = models.DateField(auto_now_add=True)
    visits = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.date} - {self.visits}"