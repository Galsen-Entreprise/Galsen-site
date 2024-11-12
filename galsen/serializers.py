from rest_framework import serializers
from .models import CustomUser, Profil, Experience, Formation, Post, MediasPost, Commentaire, Share, Reponse, Job, ShareJob, Boutique, Client, Product, Commande, ReponseCommande, MediasProduct, Notification, Facture, Annonce

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class ProfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profil
        fields = '__all__'

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'

class FormationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formation
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class MediasPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediasPost
        fields = '__all__'
        
class CommentaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentaire
        fields = '__all__'
        
class ShareSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Share
        fields = '__all__'
        
class ReponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reponse
        fields = '__all__'
        
class AnnonceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annonce
        fields = '__all__'
        
class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
        
class ShareJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShareJob
        fields = '__all__'
        
class BoutiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boutique
        fields = '__all__'
        
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        
class MediasProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediasProduct
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    medias = MediasProductSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        
class CommandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commande
        fields = '__all__'
        
class FactureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facture
        fields = '__all__'
        
class ReponseCommandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReponseCommande
        fields = '__all__'
        
class MediasProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediasProduct
        fields = '__all__'
        
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'