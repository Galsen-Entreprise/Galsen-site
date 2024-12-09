from itertools import islice
from django.http import HttpResponse, HttpResponseNotFound
from django.utils import timezone
from django.db import models
from django.http import HttpResponseRedirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
import os
import time
from django.http import JsonResponse
from django.db.models import Q
from django.views import View
from galsen.utils import obtenir_marque_dispositif
from django.forms import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .decorators import role_required
from django.db.models import Case, When, Value, IntegerField

''' =========== Les API ========= '''
from rest_framework import viewsets
from .serializers import AnnonceSerializer, CustomUserSerializer, FactureSerializer, PostSerializer, MediasPostSerializer, JobSerializer, BoutiqueSerializer, CommentaireSerializer, ReponseSerializer, ProductSerializer, MediasProductSerializer, ProfilSerializer, ExperienceSerializer, FormationSerializer, NotificationSerializer, CommandeSerializer

''' =========== Les Models ========= '''
from .models import Annonce, CustomUser, Facture, Post, MediasPost, Job, Boutique, Commentaire, Reponse, Product, MediasProduct, Profil, Experience, Formation, Notification, Commande, Traffic

''' =========== Authentication ========= '''
from django.contrib.auth import authenticate, login, logout
from galsen.forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import viewsets
from .serializers import CustomUserSerializer
from .forms import EmailChangeForm, NameChangeForm, RoleChangeForm, AccountDeleteForm, PasswordChangeForm

# Create your views here.

''' =========== Les API ========= '''
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
class MediasPostViewSet(viewsets.ModelViewSet):
    queryset = MediasPost.objects.all()
    serializer_class = MediasPostSerializer

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

class BoutiqueViewSet(viewsets.ModelViewSet):
    queryset = Boutique.objects.all()
    serializer_class = BoutiqueSerializer

class CommentaireViewSet(viewsets.ModelViewSet):
    queryset = Commentaire.objects.all()
    serializer_class = CommentaireSerializer

class ReponseViewSet(viewsets.ModelViewSet):
    queryset = Reponse.objects.all()
    serializer_class = ReponseSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class MediasProductViewSet(viewsets.ModelViewSet):
    queryset = MediasProduct.objects.all()
    serializer_class = MediasProductSerializer

class ProfilViewSet(viewsets.ModelViewSet):
    queryset = Profil.objects.all()
    serializer_class = ProfilSerializer

class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer

class FormationViewSet(viewsets.ModelViewSet):
    queryset = Formation.objects.all()
    serializer_class = FormationSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class CommandeViewSet(viewsets.ModelViewSet):
    queryset = Commande.objects.all()
    serializer_class = CommandeSerializer
    
class FactureViewSet(viewsets.ModelViewSet):
    queryset = Commande.objects.all()
    serializer_class = FactureSerializer
    
class AnnonceViewSet(viewsets.ModelViewSet):
    queryset = Commande.objects.all()
    serializer_class = AnnonceSerializer


def log_in(request):
    if request.method == 'POST':
        email = request.POST['email']  
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)
        if user is not None and user.is_authenticated:
            login(request, user)
            
            # Enregistrer le trafic
            today = timezone.now().date()
            traffic, created = Traffic.objects.get_or_create(date=today)
            traffic.visits += 1  # Incrémente le nombre de visites
            traffic.save()

            roles_valides = ['admin', 'professionnel', 'ecole', 'entreprise']

            if user.rôle == 'admin':
                return redirect('SuperAdmin')
            else:
                return redirect('home')

    return render(request, 'auth/login.html')

def login_admin(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        user = authenticate(request, username=request.user.username, password=password)
        if user is not None:
            # Mot de passe validé, redirige vers SuperAdmin
            return redirect('SuperAdmin')
        else:
            # Mot de passe incorrect
            messages.error(request, "Mot de passe incorrect. Veuillez réessayer.")

    return render(request, 'auth/login_admin.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        try:
            form.full_clean()  # Utilisez full_clean pour déclencher toutes les validations du formulaire
        except ValidationError as e:
            
            for field, messages in e.message_dict.items():
                form.add_error(field, messages)
        if form.is_valid():
            user = form.save()
            user.backend = 'galsen.backends.EmailBackend'
            login(request, user)
            
            user_role = request.user.rôle

            if user_role == 'admin':
                return render(request, '')
            elif user_role == 'professionnel':
                return render(request, 'auth/professionnel.html')
            elif user_role == 'ecole':
                return render(request, 'auth/ecole.html')
            elif user_role == 'entreprise':
                return render(request, 'auth/entreprise.html')
    else:
        form = CustomUserCreationForm()

    return render(request, 'auth/register.html', {'form': form})

def log_out(request):
    # pass
    logout(request)
    messages.success(request, 'Déconnecter👌🏾')
    return redirect('login')

def profile(request):
    if request.method == 'POST':
        user = request.user
        
        # Récupérer les données du formulaire POST
        pays = request.POST.get('pays')
        ville = request.POST.get('ville')
        quartier = request.POST.get('quartier')
        indicatif = request.POST.get('indicatif')
        phone = request.POST.get('phone')
        number_whatsapp = request.POST.get('number_whatsapp')
        number_telegram = request.POST.get('number_telegram')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        birthday = request.POST.get('birthday')

        # Mettre à jour les champs appropriés
        user.pays = pays
        user.ville = ville
        user.quartier = quartier
        user.indicatif_pays = indicatif
        user.number_phone = phone
        user.number_whatsapp = number_whatsapp
        user.number_telegram = number_telegram

        # Vérifier si les champs first_name et last_name sont fournis, sinon les définir sur None
        user.first_name = firstname if firstname else None
        user.last_name = lastname if lastname else None

        user.birthday = birthday

        user.save()

        messages.success(request, 'Profil mis à jour avec succès.')

        return redirect('login')

''' =========== Les Pages (home, professionnel, entreprise, ecole, emplois, boutique) ========= '''
@role_required(['admin','professionnel', 'ecole', 'entreprise'])
def home(request):
    # Récupérer tous les posts avec les médias associés, les utilisateurs, et la date de création
    posts = Post.objects.select_related('user').prefetch_related('mediaspost_set').order_by('-date_creation_post').all()
    user = request.user
    
    if request.method == "GET":
        contenu_post = request.GET.get('poste')
        if contenu_post is not None:
            posts = Post.objects.filter(contenu_post__icontains=contenu_post)
    
    if request.user.is_authenticated:
        marque_dispositif = obtenir_marque_dispositif(request)
        request.user.marque_dispositif = marque_dispositif
        request.user.save()

    context = {
        'posts': posts,
        'user': user
    }
    return render(request, 'pages/home.html', context)

@role_required(['admin','professionnel', 'ecole', 'entreprise'])
def professionnel(request):
    CustomUsers = CustomUser.objects.filter(rôle='professionnel')
    user = request.user
    query = request.GET.get('professionnel')

    if query:
        # Séparer le query en mots individuels pour rechercher dans first_name, last_name et rôle
        query_words = query.split()

        # Construire une requête qui recherche dans first_name, last_name et rôle indépendamment de l'ordre
        filter_query = Q()
        for word in query_words:
            filter_query &= (
                Q(first_name__icontains=word) | 
                Q(last_name__icontains=word) |
                Q(metier__icontains=word)
            )

        CustomUsers = CustomUser.objects.filter(rôle='professionnel').filter(filter_query)

    context = {
        'CustomUsers': CustomUsers,
        'user': user,
        'query': query,  # Ajouter la requête pour la réafficher dans le formulaire
        'result_count': CustomUsers.count()
    }
    return render(request, 'pages/professionnel.html', context)

@role_required(['admin','professionnel', 'ecole', 'entreprise'])
def entreprise(request):
    CustomUsers = CustomUser.objects.filter(rôle='entreprise')
    user = request.user
    query = request.GET.get('entreprise')

    if query:
        # Séparer le query en mots individuels pour rechercher dans first_name, last_name et rôle
        query_words = query.split()

        # Construire une requête qui recherche dans first_name, last_name et rôle indépendamment de l'ordre
        filter_query = Q()
        for word in query_words:
            filter_query &= ( 
                Q(etablissement__icontains=word) |
                Q(metier__icontains=word)
            )

        CustomUsers = CustomUser.objects.filter(rôle='entreprise').filter(filter_query)

    context = {
        'CustomUsers': CustomUsers,
        'user': user,
        'query': query,  # Ajouter la requête pour la réafficher dans le formulaire
        'result_count': CustomUsers.count()
    }
    return render(request, 'pages/entreprise.html', context)

@role_required(['admin','professionnel', 'ecole', 'entreprise'])
def ecole(request):
    CustomUsers = CustomUser.objects.filter(rôle='ecole')
    user = request.user
    query = request.GET.get('ecole')

    if query:
        # Séparer le query en mots individuels pour rechercher dans first_name, last_name et rôle
        query_words = query.split()

        # Construire une requête qui recherche dans first_name, last_name et rôle indépendamment de l'ordre
        filter_query = Q()
        for word in query_words:
            filter_query &= ( 
                Q(etablissement__icontains=word) |
                Q(metier__icontains=word)
            )

        CustomUsers = CustomUser.objects.filter(rôle='ecole').filter(filter_query)

    context = {
        'CustomUsers': CustomUsers,
        'user': user,
        'query': query,  # Ajouter la requête pour la réafficher dans le formulaire
        'result_count': CustomUsers.count()
    }
    return render(request, 'pages/ecole.html', context)

def annonce(request):
    user = request.user
    
    annonces = Annonce.objects.select_related('user').order_by('-date_creation')
    
    if request.method == "GET":
        title = request.GET.get('service')
        if title is not None:
            annonces = annonces.filter(title__icontains=title)
            
    context = {
        'annonces': annonces,
        'user': user
    }
    return render(request, 'pages/annonces.html', context)

@role_required(['admin','professionnel', 'ecole', 'entreprise'])
def emplois(request):
     # Récupérer l'utilisateur connecté
    user = request.user
    
    # Récupérer les offres d'emploi
    jobs = Job.objects.select_related('user').order_by('-date_creation_post').exclude(postule_job=user)
    
    if request.method == "GET":
        title = request.GET.get('job')
        if title is not None:
            jobs = jobs.filter(title__icontains=title)

    context = {
        'jobs': jobs,
        'user': user
    }
    return render(request, 'pages/emplois.html', context)

@role_required(['admin','professionnel', 'ecole', 'entreprise'])
def boutique(request):
    # Récupérer l'utilisateur connecté
    user = request.user

    # Récupérer tous les produits disponibles
    produits_disponibles = Product.objects.all()

    # Gestion de la recherche
    recherche = request.GET.get('boutique')
    if recherche:
        # Nettoyage de la recherche (sans majuscules, sans accents)
        recherche = recherche.lower()

        # Construire une requête insensible aux accents et majuscules
        produits = produits_disponibles.filter(
            Q(nom_produit__icontains=recherche) |
            Q(category__icontains=recherche)
        )
    else:
        # Si aucune recherche n'est active, afficher tous les produits
        produits = produits_disponibles

    # Contexte pour le template
    context = {
        'user': user,
        'produits': produits,
        'recherche_active': bool(recherche),
    }

    return render(request, 'pages/boutique.html', context)



''' =========== Section Admin ========= '''
def SuperAdmin(request):
    # Récupérer la date d'aujourd'hui en tenant compte du fuseau horaire
    today = timezone.now().date()
    
    # Récupérer le nombre de visites d'aujourd'hui
    traffic_count = Traffic.objects.filter(date=today).aggregate(total_visits=models.Sum('visits'))['total_visits'] or 0

    # Compter le nombre d'utilisateurs selon leur rôle
    admin_count = CustomUser.objects.filter(access='autorised').count()
    professionnel_count = CustomUser.objects.filter(rôle='professionnel').count()
    ecole_count = CustomUser.objects.filter(rôle='ecole').count()
    entreprise_count = CustomUser.objects.filter(rôle='entreprise').count()
    
    # Compter le nombre total d'utilisateurs
    total_users_count = CustomUser.objects.count()
    
    # Compter le nombre de boutiques
    boutique_count = Boutique.objects.count()

    # Calculer le pourcentage pour chaque rôle
    def calculate_percentage(count):
        return (count / total_users_count * 100) if total_users_count > 0 else 0

    admin_percentage = calculate_percentage(admin_count)
    professionnel_percentage = calculate_percentage(professionnel_count)
    ecole_percentage = calculate_percentage(ecole_count)
    entreprise_percentage = calculate_percentage(entreprise_count)

    # Récupérer les données de trafic mensuel pour l'année actuelle et l'année précédente
    current_year = today.year
    previous_year = current_year - 1

    monthly_current_year = Traffic.objects.filter(date__year=current_year).values('date__month').annotate(total_visits=models.Sum('visits')).order_by('date__month')
    monthly_previous_year = Traffic.objects.filter(date__year=previous_year).values('date__month').annotate(total_visits=models.Sum('visits')).order_by('date__month')

    # Créer des tableaux pour stocker les visites mensuelles
    current_year_visits = [0] * 12
    previous_year_visits = [0] * 12

    for entry in monthly_current_year:
        month = entry['date__month'] - 1
        current_year_visits[month] = entry['total_visits']

    for entry in monthly_previous_year:
        month = entry['date__month'] - 1
        previous_year_visits[month] = entry['total_visits']

    context = {
        'traffic_count': traffic_count,
        'admin_count': admin_count,
        'admin_percentage': admin_percentage,
        'professionnel_count': professionnel_count,
        'professionnel_percentage': professionnel_percentage,
        'ecole_count': ecole_count,
        'ecole_percentage': ecole_percentage,
        'entreprise_count': entreprise_count,
        'entreprise_percentage': entreprise_percentage,
        'total_users_count': total_users_count,
        'boutique_count': boutique_count,
        'current_year_visits': current_year_visits,
        'previous_year_visits': previous_year_visits,
        'previous_year': previous_year,  # Passer l'année précédente au template
    }
    
    return render(request, 'admins/dashboard.html', context)

def adminadmin(request):
    CustomUsers = CustomUser.objects.filter(access='autorised')
    access_count = CustomUser.objects.filter(access='autorised').count()
    user = request.user

    context = {
        'CustomUsers': CustomUsers,
        'access_count': access_count,
        'user': user
    }
    return render(request, 'admins/details/admin.html', context)

def adminprofessionnel(request):
    CustomUsers = CustomUser.objects.filter(rôle='professionnel')
    professionnel_count = CustomUser.objects.filter(rôle='professionnel').count()
    user = request.user

    context = {
        'CustomUsers': CustomUsers,
        'professionnel_count': professionnel_count,
        'user': user
    }
    return render(request, 'admins/details/professionnel.html', context)

def adminentreprise(request):
    CustomUsers = CustomUser.objects.filter(rôle='entreprise')
    entreprise_count = CustomUser.objects.filter(rôle='entreprise').count()
    user = request.user

    context = {
        'CustomUsers': CustomUsers,
        'entreprise_count': entreprise_count,
        'user': user
    }
    return render(request, 'admins/details/entreprise.html', context)

def adminecole(request):
    CustomUsers = CustomUser.objects.filter(rôle='ecole')
    ecole_count = CustomUser.objects.filter(rôle='ecole').count()
    user = request.user

    context = {
        'CustomUsers': CustomUsers,
        'ecole_count': ecole_count,
        'user': user
    }
    return render(request, 'admins/details/ecole.html', context)

def adminusers(request):
    CustomUsers = CustomUser.objects.order_by('-date_joined').all()
    user_count = CustomUser.objects.count()
    user = request.user

    context = {
        'CustomUsers': CustomUsers,
        'user_count': user_count,
        'user': user
    }
    return render(request, 'admins/details/users.html', context)

def change_user(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    
    if request.method == 'POST':
        # Récupérer les données du formulaire
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.langue = request.POST.get('langue', user.langue)
        user.rôle = request.POST.get('rôle', user.rôle)
        user.genre = request.POST.get('genre', user.genre)
        user.situation_matrimoniale = request.POST.get('situation_matrimoniale', user.situation_matrimoniale)
        user.pays = request.POST.get('pays', user.pays)
        user.ville = request.POST.get('ville', user.ville)
        user.quartier = request.POST.get('quartier', user.quartier)
        user.number_phone = request.POST.get('number_phone', user.number_phone)
        user.number_whatsapp = request.POST.get('number_whatsapp', user.number_whatsapp)
        user.number_telegram = request.POST.get('number_telegram', user.number_telegram)
        user.metier = request.POST.get('metier', user.metier)
        user.etablissement = request.POST.get('etablissement', user.etablissement)
        user.birthday = request.POST.get('birthday', user.birthday)
        user.instagram_link = request.POST.get('instagram_link', user.instagram_link)
        user.twitter_link = request.POST.get('twitter_link', user.twitter_link)
        user.youtube_link = request.POST.get('youtube_link', user.youtube_link)
        user.website_link = request.POST.get('website_link', user.website_link)

        # Gérer les fichiers téléchargés (photo de profil et bannière)
        if 'profile_image' in request.FILES:
            user.profile_image = request.FILES['profile_image']
        if 'banner_image' in request.FILES:
            user.banner_image = request.FILES['banner_image']
        
        # Sauvegarder les modifications
        user.save()
        messages.success(request, "Les informations de l'utilisateur ont été mises à jour avec succès.")
        return redirect('SuperAdmin')
    
    return render(request, 'admins/formulaires/change_user.html', {'change_user': user})

def delete_user(request, user_id):
    user_to_delete = get_object_or_404(CustomUser, id=user_id)

    # Vérifier si l'utilisateur actuel est admin ou est l'utilisateur qu'il souhaite supprimer
    if request.user.is_staff or user_to_delete == request.user:
        user_to_delete.delete()
        messages.success(request, 'Utilisateur supprimé avec succès.')
    else:
        messages.error(request, 'Vous n\'avez pas l\'autorisation de supprimer ce compte.')

    # Rediriger vers une page de confirmation ou la page d'accueil après suppression
    return redirect('SuperAdmin') 
''' =========== Formulaires ========= '''
@role_required(['admin','professionnel', 'ecole', 'entreprise'])
def create_post(request):
    if request.method == 'POST':
        contenu_post = request.POST.get('contenu_post')
        tag_post = request.POST.get('tag_post')
        video = request.FILES.get('video')
        
        # Obtenez les informations de session actuelles
        session_info = obtenir_marque_dispositif(request)

        # Créez un nouveau post avec les informations de session
        new_post = Post.objects.create(
            user=request.user,
            contenu_post=contenu_post,
            tag_post=tag_post,
            video=video,
            session_info=session_info
        )

        # Récupérer les fichiers images envoyés
        images = request.FILES.getlist('image')

        # Itérer sur chaque image et les enregistrer dans la base de données
        for image_file in images:
            MediasPost.objects.create(
                post=new_post,
                image=image_file
            )
    
        user_role = request.user.rôle
        messages.success(request, 'Poste créé avec succès!')

        if user_role == 'admin':
            return redirect('Ad_posts')
        else:
            return redirect('home')
    
    return render(request, 'formulaires/post.html')

@role_required(['admin','professionnel', 'ecole', 'entreprise'])
def create_job(request):
    if request.method == 'POST':
        contenu_job = request.POST.get('contenu_job')
        title = request.POST.get('title')
    
        newJob = Job.objects.create(
            user=request.user,
            contenu_job=contenu_job, 
            title=title
            )
    
    
        user_role = request.user.rôle
        
        if user_role == 'admin':
            return redirect('Ad_posts')
        else:
            return redirect('emplois')
        
    return render(request, 'formulaires/job.html')

def create_annonce(request):
    if request.method == 'POST':
        contenu_text = request.POST.get('contenu_text')
        service = request.POST.get('service')
        prix = request.POST.get('prix')
        image = request.FILES.get('image')

        # Créez un nouveau post avec les informations de session
        new_annonce = Annonce.objects.create(
            user=request.user,
            contenu_text=contenu_text,
            service=service,
            prix=prix,
            image=image,
        )
    
        user_role = request.user.rôle
        messages.success(request, 'Annonce créé avec succès!')

        if user_role == 'admin':
            return redirect('Ad_posts')
        else:
            return redirect('annonce')
    return render(request, 'formulaires/annonce.html')

class AddPostule(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        job = get_object_or_404(Job, pk=pk)

        # Vérifier si l'utilisateur a déjà aimé ou n'aime pas le poste
        is_dispostule = job.dispostule.filter(pk=request.user.pk).exists()
        is_postule = job.postule_job.filter(pk=request.user.pk).exists()

        # Si l'utilisateur n'aime pas le poste, le retirer de la liste des dislikes
        if is_dispostule:
            job.dispostule.remove(request.user)

        # Si l'utilisateur n'a pas déjà aimé le poste, l'ajouter aux likes
        if not is_postule:
            job.postule_job.add(request.user)
            postule_icon = '<i class="fa fa-thumbs-up primary"></i>'
        # Si l'utilisateur a déjà aimé le poste, le retirer des likes
        else:
            job.postule_job.remove(request.user)
            postule_icon = '<i class="fa fa-thumbs-up"></i>'

        # Renvoyer les informations mises à jour
        response_data = {
            'like_count': job.postule_job.count(),
            'postule_icon': postule_icon,
        }
        
        user_role = request.user.rôle
        if user_role == 'admin':
            return redirect('Ad_job')
        else:
            return redirect('emplois')

def create_boutique(request):
    if request.method == 'POST':
        # Récupère l'utilisateur connecté
        user = request.user
        
        # Récupère les données du formulaire
        nom_boutique = request.POST.get('nom_boutique')
        devise_boutique = request.POST.get('devise_boutique')
        
        # Crée un nouvel objet Boutique
        nouvelle_boutique = Boutique.objects.create(
            user=user,
            nom_boutique=nom_boutique,
            devise_boutique=devise_boutique
        )
        
        # Redirige vers la vue pour gérer la boutique
        return redirect('En_Gestion_Boutique')
        
    return render(request, 'auth/boutique.html')

def create_product(request):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        description = request.POST.get('description')
        nom_produit = request.POST.get('nom_produit')
        prix = request.POST.get('prix')
        video = request.FILES.get('video')
        category = request.POST.get('category')  # Récupérer la catégorie
        images = request.FILES.getlist('image')  # Récupérer les fichiers images envoyés

        # Récupérer l'utilisateur actuel
        utilisateur = request.user
        
        # Récupérer la boutique associée à l'utilisateur actuel
        boutique = Boutique.objects.get(user=utilisateur)
        
        # Créer un nouveau produit
        new_product = Product.objects.create(
            boutique=boutique,
            description=description,
            nom_produit=nom_produit,
            prix=prix,
            video=video,
            category=category  # Ajouter la catégorie
        )
        
        # Enregistrer chaque image comme un objet MediasProduct
        for image in images:
            MediasProduct.objects.create(
                produit=new_product,
                image=image
            )
        
        # Rediriger l'utilisateur après la création du produit
        return redirect('En_Gestion_Boutique')
        
    return render(request, 'formulaires/product.html')

def facture(request):
    factures = Facture.objects.filter(user=request.user)
    
    # Vérifier si toutes les factures sont partagées
    all_shared = factures.filter(is_public=False).count() == 0
    
    if request.method == "POST":
        if 'share_all' in request.POST:
            # Partager toutes les factures de l'utilisateur
            factures.update(is_public=True)
            
            # Envoyer la notification après le partage
            users_with_public_invoices = CustomUser.objects.filter(
                pays=request.user.pays,
                quartier=request.user.quartier,
                ville=request.user.ville
            )
            # Créer une notification pour chaque utilisateur
            for user in users_with_public_invoices:
                Notification.objects.create(user=user, message=f"{request.user.username} a partagé ses factures.")

        elif 'unshare_all' in request.POST:
            # Ne plus partager toutes les factures de l'utilisateur
            factures.update(is_public=False)

        return redirect('facture')

    return render(request, 'formulaires/facture.html', {'factures': factures, 'all_shared': all_shared})

''' =========== CV: Update profile, Create experience, Update experience, Create Formation, Update Formation ========= '''
@role_required(['admin','professionnel', 'ecole', 'entreprise'])
def a_propos(request):
    # Récupérer l'utilisateur actuel
    user = request.user
    
    # Récupérer le profil de l'utilisateur s'il existe
    try:
        profil = Profil.objects.get(user=user)
    except Profil.DoesNotExist:
        profil = None
    
    # Récupérer l'expérience de l'utilisateur s'il existe
    try:
        experience = Experience.objects.get(user=user)
    except Experience.DoesNotExist:
        experience = None
    
    # Récupérer la formation de l'utilisateur si elle existe
    try:
        formation = Formation.objects.get(user=user)
    except Formation.DoesNotExist:
        formation = None
    
    # Charger le template de mise à jour correspondant au rôle de l'utilisateur
    user_role = user.rôle
    if user_role == 'admin':
        return render(request, 'profils/a_propos.html', {'user': user, 'profil': profil, 'experience': experience, 'formation': formation})
    else:
        return render(request, 'profils/a_propos.html', {'user': user, 'profil': profil, 'experience': experience, 'formation': formation})

def update_cv_profil(request):
    if request.method == 'POST':
        # Récupérez la description mise à jour depuis le formulaire
        description = request.POST.get('description')

        # Vérifiez si l'utilisateur a un profil existant
        if hasattr(request.user, 'profil'):
            # Mettez à jour la description du profil existant
            request.user.profil.description = description
            request.user.profil.save()
        else:
            # Créez un nouveau profil si l'utilisateur n'en a pas encore
            Profil.objects.create(user=request.user, description=description)

        # Rediriger l'utilisateur vers la page 'a_propos' après la mise à jour du profil
        return redirect('a_propos')
            
    else:    
        # Récupérer le profil de l'utilisateur
        profil = getattr(request.user, 'profil', None)
        context = {'profil': profil}
        return render(request, 'formulaires/update/cv/profil.html', context)
    
def create_cv_experience(request):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        title = request.POST.get('title')
        description = request.POST.get('description')

        # Créer une nouvelle instance de Experience
        new_experience = Experience.objects.create(user=request.user, title=title, description=description)

        # Rediriger l'utilisateur vers une page de confirmation ou une autre vue
        return redirect('a_propos')  # Remplacez 'nom_de_la_vue_de_confirmation' par le nom de la vue de confirmation appropriée

    return render(request, 'formulaires/update/cv/experience.html')


def update_cv_experience(request, experience_id):
    # Récupérer l'expérience à modifier
    experience = get_object_or_404(Experience, id=experience_id)

    if request.method == 'POST':
        # Récupérer les données du formulaire
        title = request.POST.get('title')
        description = request.POST.get('description')

        # Mettre à jour les données de l'expérience
        experience.title = title
        experience.description = description
        experience.save()

        # Rediriger l'utilisateur vers une page de confirmation ou une autre vue
        return redirect('a_propos')  # Remplacez 'nom_de_la_vue_de_confirmation' par le nom de la vue de confirmation appropriée

    # Charger les données de l'expérience dans le formulaire
    context = {'experience': experience}
    return render(request, 'formulaires/update/cv/update_experience.html', context)

def create_cv_formation(request):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        title = request.POST.get('title')
        description = request.POST.get('description')

        # Créer une nouvelle instance de Experience
        new_formation = Formation.objects.create(user=request.user, title=title, description=description)

        # Rediriger l'utilisateur vers une page de confirmation ou une autre vue
        return redirect('a_propos')  # Remplacez 'nom_de_la_vue_de_confirmation' par le nom de la vue de confirmation appropriée

    return render(request, 'formulaires/update/cv/formation.html')

def update_cv_formation(request, formation_id):
    # Récupérer l'formation à modifier
    formation = get_object_or_404(Formation, id=formation_id)

    if request.method == 'POST':
        # Récupérer les données du formulaire
        title = request.POST.get('title')
        description = request.POST.get('description')

        # Mettre à jour les données de l'expérience
        formation.title = title
        formation.description = description
        formation.save()

        # Rediriger l'utilisateur vers une page de confirmation ou une autre vue
        return redirect('a_propos')  # Remplacez 'nom_de_la_vue_de_confirmation' par le nom de la vue de confirmation appropriée

    # Charger les données de l'expérience dans le formulaire
    context = {'formation': formation}
    return render(request, 'formulaires/update/cv/update_formation.html', context)

''' =========== Les Updates ========= '''
@role_required(['admin','professionnel', 'ecole', 'entreprise'])
def update(request):
    user_role = request.user.rôle

    if user_role == 'entreprise':
        # Charger le modèle de mise à jour
        if request.method == 'POST':
            # Récupérer les données du formulaire POST
            etablissement = request.POST.get('etablissement')
            pays = request.POST.get('pays')
            indicatif = request.POST.get('indicatif')
            ville = request.POST.get('ville')
            quartier = request.POST.get('quartier')
            number_phone = request.POST.get('number_phone')
            number_whatsapp = request.POST.get('number_whatsapp')
            number_telegram = request.POST.get('number_telegram')
            metier = request.POST.get('metier')
            birthday = request.POST.get('birthday')
            instagram_link = request.POST.get('instagram_link')
            twitter_link = request.POST.get('twitter_link')
            youtube_link = request.POST.get('youtube_link')
            website_link = request.POST.get('website_link')

            # Mettre à jour les champs appropriés
            user = request.user
            user.etablissement = etablissement
            user.pays = pays
            user.indicatif_pays = indicatif
            user.ville = ville
            user.quartier = quartier
            user.number_phone = number_phone
            user.number_whatsapp = number_whatsapp
            user.number_telegram = number_telegram
            user.metier = metier
            user.birthday = birthday
            user.instagram_link = instagram_link
            user.twitter_link = twitter_link
            user.youtube_link = youtube_link
            user.website_link = website_link
            user.save()

            # Rediriger vers 
            return redirect('detail_profile')

        # Charger le modèle de mise à jour pour l'entreprise
        return render(request, 'formulaires/update/entreprise_statut.html')
    
    elif user_role == 'professionnel':
        # Charger le modèle de mise à jour pour le professionnel
        if request.method == 'POST':
            # Récupérer les données du formulaire POST
            pays = request.POST.get('pays')
            indicatif = request.POST.get('indicatif')
            ville = request.POST.get('ville')
            quartier = request.POST.get('quartier')
            number_phone = request.POST.get('number_phone')
            number_whatsapp = request.POST.get('number_whatsapp')
            number_telegram = request.POST.get('number_telegram')
            metier = request.POST.get('metier')
            birthday = request.POST.get('birthday')
            instagram_link = request.POST.get('instagram_link')
            twitter_link = request.POST.get('twitter_link')
            youtube_link = request.POST.get('youtube_link')
            website_link = request.POST.get('website_link')

            # Mettre à jour les champs appropriés
            user = request.user
            user.pays = pays
            user.indicatif_pays = indicatif
            user.ville = ville
            user.quartier = quartier
            user.number_phone = number_phone
            user.number_whatsapp = number_whatsapp
            user.number_telegram = number_telegram
            user.metier = metier
            user.birthday = birthday
            user.instagram_link = instagram_link
            user.twitter_link = twitter_link
            user.youtube_link = youtube_link
            user.website_link = website_link
            user.save()
            
            return redirect('detail_profile')
        
        return render(request, 'formulaires/update/personnel_statut.html')

    elif user_role == 'ecole':
        # Charger le modèle de mise à jour pour l'école
        if request.method == 'POST':
            # Récupérer les données du formulaire POST
            etablissement = request.POST.get('etablissement')
            pays = request.POST.get('pays')
            indicatif = request.POST.get('indicatif')
            ville = request.POST.get('ville')
            quartier = request.POST.get('quartier')
            number_phone = request.POST.get('number_phone')
            number_whatsapp = request.POST.get('number_whatsapp')
            number_telegram = request.POST.get('number_telegram')
            metier = request.POST.get('metier')
            birthday = request.POST.get('birthday')
            instagram_link = request.POST.get('instagram_link')
            twitter_link = request.POST.get('twitter_link')
            youtube_link = request.POST.get('youtube_link')
            website_link = request.POST.get('website_link')

            # Mettre à jour les champs appropriés
            user = request.user
            user.etablissement = etablissement
            user.pays = pays
            user.indicatif_pays = indicatif
            user.ville = ville
            user.quartier = quartier
            user.number_phone = number_phone
            user.number_whatsapp = number_whatsapp
            user.number_telegram = number_telegram
            user.metier = metier
            user.birthday = birthday
            user.instagram_link = instagram_link
            user.twitter_link = twitter_link
            user.youtube_link = youtube_link
            user.website_link = website_link
            user.save()
            
            return redirect('detail_profile')
        
        return render(request, 'formulaires/update/ecole_statut.html')

    elif user_role == 'admin':
        # Charger le modèle de mise à jour pour l'admin
        if request.method == 'POST':
            # Récupérer les données du formulaire POST
            metier = request.POST.get('metier')
            pays = request.POST.get('pays')
            ville = request.POST.get('ville')
            quartier = request.POST.get('quartier')
            indicatif = request.POST.get('indicatif')
            phone = request.POST.get('phone')

            # Mettre à jour les champs appropriés
            user = request.user
            user.metier = metier
            user.pays = pays
            user.ville = ville
            user.quartier = quartier
            user.indicatif_pays = indicatif
            user.number_phone = phone  
            user.save()
            
            return redirect('Ad_profile')
        return render(request, 'formulaires/update/admin_statut.html')

    # Si aucun rôle correspondant n'est trouvé ou si la méthode de requête n'est pas POST
    return render(request, 'path_vers_votre_template_d_erreur.html')

@role_required(['admin','professionnel', 'ecole', 'entreprise'])
def update_profile(request):
    CustomUser = request.user
    if request.method == 'POST':
        user = request.user
        new_profile_image = request.FILES.get('image')

        # Supprimer l'ancienne image de la base de données et localement
        if user.profile_image:
            old_image_path = os.path.join(settings.MEDIA_ROOT, str(user.profile_image))
            os.remove(old_image_path)

        # Enregistrer la nouvelle image dans le répertoire de stockage local
        user.profile_image = new_profile_image
        user.save()

        user_role = request.user.rôle
        
        if user_role == 'admin':
            return redirect('Ad_profile')
        else:
            return redirect('detail_profile')
        # Rediriger vers la page de profil appropriée
    else:
        return render(request, 'formulaires/update/update_profile.html', {'CustomUser': CustomUser})

@role_required(['admin','professionnel', 'ecole', 'entreprise'])
def update_banner(request):
    CustomUser = request.user
    if request.method == 'POST':
        user = request.user
        new_profile_banner = request.FILES.get('banner')

        # Supprimer l'ancienne image de la base de données et localement
        if user.banner_image:
            old_image_path = os.path.join(settings.MEDIA_ROOT, str(user.banner_image))
            os.remove(old_image_path)

        # Enregistrer la nouvelle image dans le répertoire de stockage local
        user.banner_image = new_profile_banner
        user.save()

        user_role = request.user.rôle
        
        if user_role == 'admin':
            return redirect('Ad_profile')
        else:
            return redirect('detail_profile')
        # Rediriger vers la page de profil ou toute autre page appropriée
    else:
        return render(request, 'formulaires/update/update_banner.html', {'CustomUser': CustomUser})

def update_logo_boutique(request):
    if request.method == 'POST':
        # Récupérer l'utilisateur actuellement connecté
        user = request.user

        # Récupérer la boutique associée à cet utilisateur
        boutique = Boutique.objects.get(user=user)

        # Récupérer l'image du formulaire
        image = request.FILES.get('image')

        # Mettre à jour la photo de profil de la boutique
        if image:
            # Supprimer l'ancienne image de la base de données et localement
            if boutique.photo_profil:
                old_image_path = boutique.photo_profil.path
                boutique.photo_profil.delete(save=False)

            # Enregistrer la nouvelle image dans la base de données
            boutique.photo_profil = image
            boutique.save()

        # Rediriger vers une page de confirmation ou une autre vue
        return redirect('En_Gestion_Boutique')

    # Si la méthode de requête est GET, simplement renvoyer le formulaire HTML
    return render(request, 'formulaires/update/update_logo_boutique.html')
# break

# Update Banner Boutique
def update_banner_boutique(request):
    if request.method == 'POST':
        # Récupérer l'utilisateur actuellement connecté
        user = request.user

        # Récupérer la boutique associée à cet utilisateur
        boutique = Boutique.objects.get(user=user)

        # Récupérer l'image du formulaire
        image = request.FILES.get('image')

        # Mettre à jour la photo de profil de la boutique
        if image:
            # Supprimer l'ancienne image de la base de données et localement
            if boutique.banner_image:
                old_image_path = boutique.banner_image.path
                boutique.banner_image.delete(save=False)

            # Enregistrer la nouvelle image dans la base de données
            boutique.banner_image = image
            boutique.save()

        # Rediriger vers une page de confirmation ou une autre vue
        return redirect('En_Gestion_Boutique')

    # Si la méthode de requête est GET, simplement renvoyer le formulaire HTML
    return render(request, 'formulaires/update/update_banner_boutique.html')
# break

# Update Description Boutique
def update_description_boutique(request):
    if request.method == 'POST':
        # Récupérer l'utilisateur actuellement connecté
        user = request.user

        # Récupérer la boutique associée à cet utilisateur
        boutique = Boutique.objects.get(user=user)

        
        description = request.POST.get('description')

        

        boutique.description = description
        boutique.save()

        # Rediriger vers une page de confirmation ou une autre vue
        return redirect('En_Gestion_Boutique')

    # Si la méthode de requête est GET, simplement renvoyer le formulaire HTML
    return render(request, 'formulaires/update/update_description_boutique.html')
# break

def update_post(request, id):
    post = get_object_or_404(Post, id=id)
    medias_post = MediasPost.objects.filter(post=post).first()

    if request.method == 'POST':
        post.contenu_post = request.POST['contenu_post']
        post.tag_post = request.POST['tag_post']
        post.save()

        # Récupérer les fichiers téléchargés
        new_image_file = request.FILES.get('image')
        new_video_file = request.FILES.get('video')

        # Si un nouveau fichier image est fourni, supprimer l'ancienne image
        if new_image_file:
            if medias_post and medias_post.image and os.path.exists(medias_post.image.path):
                medias_post.image.delete(save=False)
            # Mettre à jour ou créer l'image associée
            if medias_post:
                medias_post.image = new_image_file
                medias_post.save()
            else:
                MediasPost.objects.create(post=post, image=new_image_file)

        # Si un nouveau fichier vidéo est fourni, supprimer l'ancienne vidéo
        if new_video_file:
            if post.video and os.path.exists(post.video.path):
                post.video.delete(save=False)
            post.video = new_video_file
            post.save()

        # Redirection après la mise à jour
        user_role = request.user.rôle  
        if user_role == 'admin':
            return redirect('Ad_profile')
        else:
            return redirect('detail_profile')

    return render(request, 'formulaires/update/update_post.html', {'post': post, 'medias_post': medias_post})

def update_annonce(request, annonce_id):
    annonce = get_object_or_404(Annonce, id=annonce_id)
    if request.method == 'POST':
        # Récupérer les données du formulaire
        image = request.FILES.get('image')
        contenu_text = request.POST.get('contenu_text')
        service = request.POST.get('service')
        prix = request.POST.get('prix')

        # Mettre à jour les données de l'expérience
        if image:
            # Supprimer l'ancienne image de la base de données et localement
            if annonce.image:
                old_image_path = annonce.image.path
                annonce.image.delete(save=False)
                
        annonce.image = image
        annonce.contenu_text = contenu_text
        annonce.service = service
        annonce.prix = prix
        annonce.save()

        user_role = request.user.rôle  
        if user_role == 'admin':
            return redirect('Ad_profile')
        else:
            return redirect('annonce')
        
    # Charger les données de l'expérience dans le formulaire
    context = {'annonce': annonce}
    
    return render(request, 'formulaires/update/update_annonce.html', context)

def update_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == 'POST':
        # Récupérer les données du formulaire
        title = request.POST.get('title')
        contenu_job = request.POST.get('contenu_job')

        # Mettre à jour les données de l'expérience
        job.title = title
        job.contenu_job = contenu_job
        job.save()

        user_role = request.user.rôle  
        if user_role == 'admin':
            return redirect('Ad_profile')
        else:
            return redirect('emplois')
        
    # Charger les données de l'expérience dans le formulaire
    context = {'job': job}
    
    return render(request, 'formulaires/update/update_job.html', context)

def update_product(request, id):
    product = get_object_or_404(Product, id=id)
    medias_product = MediasProduct.objects.filter(produit=product).first()

    if request.method == 'POST':
        product.nom_produit = request.POST['nom_produit']
        product.description = request.POST['description']
        product.prix = request.POST['prix']
        product.category = request.POST['category']
        product.save()

        new_image_file = request.FILES.get('image')
        new_video_file = request.FILES.get('video')

        # Supprimer l'ancienne image seulement si une nouvelle est fournie
        if new_image_file and medias_product and medias_product.image and os.path.exists(medias_product.image.path):
            medias_product.image.delete(save=False)

        # Supprimer l'ancienne vidéo seulement si une nouvelle est fournie
        if new_video_file and product.video and os.path.exists(product.video.path):
            product.video.delete(save=False)

        # Mettre à jour les fichiers uniquement si de nouveaux fichiers sont fournis
        if new_video_file:
            product.video = new_video_file
        product.save()

        if medias_product:
            if new_image_file:
                medias_product.image = new_image_file
            medias_product.save()
        else:
            if new_image_file:
                MediasProduct.objects.create(produit=product, image=new_image_file)

        # Rediriger en fonction du rôle de l'utilisateur
        user_role = request.user.rôle  
        if user_role == 'admin':
            return redirect('Ad_profile')
        else:
            return redirect('En_Gestion_Boutique')
    
    return render(request, 'formulaires/update/update_product.html', {'product': product, 'medias_product': medias_product})

def delete_product(request, id):
    # Récupérer le produit à supprimer
    product = get_object_or_404(Product, id=id)
    
    # Récupérer les médias associés
    medias = MediasProduct.objects.filter(produit=product)

    # Supprimer les fichiers d'image associés en local
    for media in medias:
        if media.image and os.path.exists(media.image.path):
            os.remove(media.image.path)
        # Supprimer l'enregistrement de l'image de la base de données
        media.delete()

    # Supprimer le fichier vidéo si nécessaire
    if product.video and os.path.exists(product.video.path):
        os.remove(product.video.path)

    # Supprimer le produit de la base de données
    product.delete()

    # Rediriger l'utilisateur après la suppression
    return redirect('En_Gestion_Boutique')

def delete_post(request, id):
    post = get_object_or_404(Post, id=id)
    medias_post = MediasPost.objects.filter(post=post).first()

    if medias_post and medias_post.image and os.path.exists(medias_post.image.path):
        medias_post.image.delete()

    if post.video:
        # Ajoutez une pause pour laisser le temps au système de libérer le fichier
        time.sleep(1)
        
        if os.path.exists(post.video.path):
            post.video.delete()

    post.delete()

    user_role = request.user.rôle  
    if user_role == 'admin':
        return redirect('Ad_profile')
    else:
        return redirect('detail_profile')

def delete_job(request, id):
    job = get_object_or_404(Job, id=id)

    job.delete()

    user_role = request.user.rôle
    if user_role == 'admin':
        return redirect('Ad_profile')
    else:
        return redirect('emplois')
    
def delete_annonce(request, id):
    annonce = get_object_or_404(Annonce, id=id)

    # Supprimer l'image si elle existe
    if annonce.image:
        if os.path.exists(annonce.image.path):
            annonce.image.delete()  # Appeler la méthode delete()

    # Supprimer l'annonce
    annonce.delete()

    # Rediriger en fonction du rôle de l'utilisateur
    user_role = request.user.rôle
    if user_role == 'admin':
        return redirect('Ad_profile')
    else:
        return redirect('emplois')

''' =========== Les Likes ========= '''       
class AddLikes(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)

        # Vérifier si l'utilisateur a déjà aimé ou n'aime pas le poste
        is_dislike = post.dislike.filter(pk=request.user.pk).exists()
        is_like = post.like_post.filter(pk=request.user.pk).exists()

        # Si l'utilisateur n'aime pas le poste, le retirer de la liste des dislikes
        if is_dislike:
            post.dislike.remove(request.user)

        # Si l'utilisateur n'a pas déjà aimé le poste, l'ajouter aux likes
        if not is_like:
            post.like_post.add(request.user)
            like_icon = '<i class="fa fa-thumbs-up primary"></i>'
        # Si l'utilisateur a déjà aimé le poste, le retirer des likes
        else:
            post.like_post.remove(request.user)
            like_icon = '<i class="fa fa-thumbs-up"></i>'

        # Renvoyer les informations mises à jour
        response_data = {
            'like_count': post.like_post.count(),
            'like_icon': like_icon,
        }
        return JsonResponse(response_data)
    
def following_view(request):
    user = request.user
    following_users = user.get_following()
    return render(request, 'Details/abonnement.html', {'following_users': following_users})

def abonner(request):
    # Récupérer l'utilisateur actuel
    user = request.user
    # Récupérer la liste des abonnés de l'utilisateur actuel
    abonnes = user.get_followers()
    return render(request, 'Details/abonner.html', {'abonnes': abonnes})

def abonnementId(request, abonnementId):
    # Récupérez l'utilisateur par son ID d'abonnement
    utilisateur = get_object_or_404(CustomUser, id=abonnementId)
    
    # Récupérez la liste des utilisateurs suivis par l'utilisateur spécifique
    following_users = utilisateur.following_users.all()  # Assurez-vous que following_users est correctement défini dans votre modèle
    
    context = {
        'utilisateur': utilisateur,
        'following_users': following_users,
    }
    
    return render(request, 'Details/abonnementid.html', context)

def abonnerId(request, abonnerId):
    # Récupérez l'utilisateur par son ID d'abonnement
    utilisateur = get_object_or_404(CustomUser, id=abonnerId)
    
    # Récupérez la liste des abonnés de l'utilisateur spécifique
    abonnes = utilisateur.followers.all()  # Assurez-vous que abonnes est correctement défini dans votre modèle
    
    context = {
        'utilisateur': utilisateur,
        'abonnes': abonnes,
    }
    
    return render(request, 'Details/abonnerid.html', context)

def suivre_utilisateur(request, user_id):
    if request.method == 'POST':
        # Récupérer l'utilisateur cible
        user_to_follow = get_object_or_404(CustomUser, pk=user_id)
        
        # Vérifier si l'utilisateur actuel suit déjà l'utilisateur cible
        if user_to_follow.followers.filter(id=request.user.id).exists():
            # Si oui, le retirer des followers
            user_to_follow.followers.remove(request.user)
            following = False
        else:
            # Sinon, l'ajouter aux followers
            user_to_follow.followers.add(request.user)
            following = True
        
        # Préparer les données de réponse
        response_data = {
            'following': following,
            'user_id': user_id,
        }

        return JsonResponse(response_data)

''' =========== Les Details (Profils, Post, Emplois) ========= '''
def detail_profile(request):
    user = request.user
    total_likes_received = user.total_likes_received()

    # Récupérer tous les posts de l'utilisateur
    posts = Post.objects.filter(user=user)

    # Récupérer les amis de l'utilisateur (assurez-vous que `get_amis` fonctionne)
    amis = user.get_amis()[:3]  # Limiter à 3 amis

    return render(request, 'profils/user.html', {
        'user': user,
        'total_likes_received': total_likes_received,
        'posts': posts,  # Passer les postes au template
        'amis': amis,  # Passer les amis limités au template
    })

def user_detail(request, user_id):
    profile_user = get_object_or_404(CustomUser, pk=user_id)
    posts = Post.objects.filter(user=profile_user)  # Récupère tous les posts de cet utilisateur

    # Récupérer les amis
    amis = profile_user.get_amis()
    total_amis = len(amis)  # Nombre total d'amis
    trois_amis = list(islice(amis, 3))  # Limiter à 3 amis pour affichage

    # Calculer les amis en commun
    amis_en_commun = profile_user.amis_en_commun(request.user)

    return render(request, 'profils/users_public.html', {
        'profile_user': profile_user,
        'posts': posts,
        'amis': trois_amis,  # Les 3 premiers amis
        'total_amis': total_amis,  # Nombre total d'amis
        'amis_en_commun': amis_en_commun,  # Nombre d'amis en commun
    })

def annonce_detail(request, annonce_id):
    annonce = get_object_or_404(Annonce, pk=annonce_id)
    return render(request, 'Details/annonce.html', {'annonce': annonce})

def job_detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    return render(request, 'Details/job.html', {'job': job})

@role_required(['entreprise'])
def En_Gestion_Boutique(request):
    try:
        # Récupérer la boutique associée à l'utilisateur connecté
        user_boutique = Boutique.objects.get(user=request.user)
        
        # Récupérer TOUS les produits associés à cette boutique
        produits = Product.objects.filter(boutique=user_boutique).order_by('-date_creation')

        # Afficher les informations dans la page profil boutique
        return render(request, 'profils/boutique.html', {
            'user_boutique': user_boutique,
            'produits': produits,
        })
    
    except Boutique.DoesNotExist:
        # Rediriger vers la page de création de boutique si elle n'existe pas
        return redirect('create_boutique')

def postulant(request):
    # Vérifiez que l'utilisateur est connecté
    if not request.user.is_authenticated:
        return redirect('login')  # Redirigez vers la page de connexion si nécessaire
    
    # Récupérez toutes les offres créées par l'utilisateur connecté
    user_jobs = Job.objects.filter(user=request.user)

    # Créez une liste combinée des postulants pour chaque offre
    postulants_data = []
    for job in user_jobs:
        for postulant in job.postule_job.all():
            postulants_data.append({
                'user': postulant,
                'job': job,
            })

    context = {
        'postulants_data': postulants_data,
    }
    return render(request, 'Details/postulant.html', context)

def mon_job(request):
    jobs = Job.objects.filter(user=request.user)
    
    context = {
        'jobs' : jobs
    }
    return render(request, 'Details/mon_job.html', context)

def mon_annonce(request):
    annonces = Annonce.objects.filter(user=request.user)
    
    context = {
        'annonces' : annonces
    }
    return render(request, 'Details/mon_annonce.html', context)

def mon_job_detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    return render(request, 'Details/mon_job_detail.html', {'job': job})

def mon_annonce_detail(request, annonce_id):
    annonce = get_object_or_404(Annonce, pk=annonce_id)
    return render(request, 'Details/mon_annonce_detail.html', {'annonce': annonce})

def vos_postule(request):
    # Récupérer les postulations de l'utilisateur connecté
    postulations = Job.objects.filter(postule_job=request.user)
    
    context = {
        'postulations': postulations,
    }
    
    return render(request, 'Details/vos_postules.html', context)

def product_detail(request, product_id):
    # Récupérer le produit spécifique et sa boutique
    produit = Product.objects.select_related('boutique').get(id=product_id)

    # Récupérer d'autres produits de la même catégorie
    produits_meme_categorie = Product.objects.filter(category=produit.category).exclude(id=product_id)[:10]

    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        if quantity > 0:
            # Vérifier si le produit est déjà dans la facture
            existing_facture = Facture.objects.filter(user=request.user, product=produit).first()
            if existing_facture:
                if 'remove' in request.POST:
                    existing_facture.delete()
                else:
                    existing_facture.quantity = quantity
                    existing_facture.save()
            else:
                Facture.objects.create(user=request.user, product=produit, quantity=quantity)
        return redirect('boutique')

    # Vérifier si le produit est dans une facture
    is_in_facture = Facture.objects.filter(user=request.user, product=produit).exists()

    # Vérifier si le produit a déjà été commandé par l'utilisateur
    in_commande = Commande.objects.filter(user=request.user, product=produit).exists()

    context = {
        'produit': produit,
        'produits_meme_categorie': produits_meme_categorie,
        'is_in_facture': is_in_facture,  # Conserver la logique de facture
        'In_commande': in_commande        # Ajouter la logique pour commande
    }
    return render(request, 'Details/product.html', context)

def vos_commande(request):
    # Récupérer les commandes de l'utilisateur connecté
    commandes = Commande.objects.filter(user=request.user)
    
    
    context = {
        'commandes': commandes
    }
    
    return render(request, 'Details/Vos_commandes.html', context)

def les_commandes(request):
    try:
        # Récupérer la boutique associée à l'utilisateur connecté
        user_boutique = Boutique.objects.get(user=request.user)

        # Récupérer les produits de la boutique
        produits_boutique = Product.objects.filter(boutique=user_boutique)

        # Récupérer les commandes associées à ces produits
        commandes = Commande.objects.filter(product__in=produits_boutique).select_related('user', 'product')

        context = {
            'user_boutique': user_boutique,
            'commandes': commandes
        }
        return render(request, 'Details/commandes.html', context)
    
    except Boutique.DoesNotExist:
        # Si la boutique n'existe pas, rediriger vers la création de boutique
        return redirect('create_boutique')

def amis(request):

    return render(request, 'Details/amis.html')

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'Details/post.html', {'post': post})

@role_required(['admin','professionnel', 'ecole', 'entreprise'])
def post_comments(request, post_id):
    
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)  # Utilisation de id=post_id pour récupérer le post
        contenu_commentaire = request.POST.get('contenu_commentaire')
        image = request.FILES.get('image')
        
        # Créez un nouvel objet Commentaire avec les données soumises
        commentaire = Commentaire.objects.create(post=post, user=request.user, contenu_commentaire=contenu_commentaire, image=image)
        
        # Redirigez l'utilisateur vers la même page ou une autre page appropriée
        #return redirect('detail_post', post_id=post_id)
    
    post = get_object_or_404(Post, id=post_id)
    comments = Commentaire.objects.filter(post=post)
    return render(request, 'Commentaire/comment_post.html', {'post': post, 'comments': comments})

# ========== Les Réponses: Commentaires ===================
@role_required(['admin','professionnel', 'ecole', 'entreprise'])
def comment_responses(request, comment_id):
    
    if request.method == 'POST':
        comment = get_object_or_404(Commentaire, id=comment_id)
        contenu_text = request.POST.get('contenu_text')
        image = request.FILES.get('image')
        
        reponse = Reponse.objects.create(commentaire=comment, user=request.user, contenu_text=contenu_text, image=image)
    
    comment = get_object_or_404(Commentaire, id=comment_id)
    responses = Reponse.objects.filter(commentaire_id=comment.id)
    return render(request, 'Commentaire/response.html', {'comment': comment, 'responses': responses})

def produit_commande(request, produit_id):
    # Récupération de l'utilisateur et du produit
    user = request.user
    produit = get_object_or_404(Product, pk=produit_id)

    if request.method == 'POST':
        # Récupérer les informations de la commande depuis le formulaire POST
        commande = request.POST.get('commande')
        precision = request.POST.get('precision')

        # Créer une nouvelle commande
        Commande.objects.create(
            product=produit, 
            user=user, 
            commande=commande, 
            precision=precision
        )

        # Rediriger en fonction du rôle de l'utilisateur
        if user.is_authenticated:
            if user.rôle == 'admin':
                return redirect('Ad_boutique')
            else:
                return redirect('boutique')

        # Si l'utilisateur n'est pas connecté, on pourrait le rediriger ici :
        return redirect('login')

    # Récupérer les commandes liées au produit et rendre la page
    commandes = Commande.objects.filter(produit=produit)
    return render(request, 'Commandes/commande.html', {'produit': produit, 'commandes': commandes})

def boutique_detail(request, boutique_id):
    # Récupérer la boutique spécifique
    boutique = get_object_or_404(Boutique, id=boutique_id)

    # Récupérer tous les produits de cette boutique
    produits = Product.objects.filter(boutique=boutique)

    # Gestion de la recherche par 'nom_produit'
    query = request.GET.get('poste')
    if query:
        produits = produits.filter(Q(nom_produit__icontains=query))

    context = {
        'boutique': boutique,
        'produits': produits,
    }
    return render(request, 'profils/boutiques.html', context)

def categorie_view(request, category):
    # Récupérer tous les produits de la catégorie sélectionnée
    produits = Product.objects.filter(category=category)
    
    # Pour déboguer, vous pouvez imprimer les catégories existantes
    print("Catégorie demandée:", category)
    print("Produits trouvés:", produits.count())

    context = {
        'produits': produits,
        'category': category,
    }
    return render(request, 'Details/categories/categorie.html', context)
   

def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None
def a_propos_detail(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    context = {'user': user}
    
    if user.rôle == 'professionnel':
        template_name = 'profils/a_propos_public.html'
        context['profil'] = get_or_none(Profil, user=user)
        context['experience'] = get_or_none(Experience, user=user)
        context['formation'] = get_or_none(Formation, user=user)
    elif user.rôle == 'entreprise':
        template_name = 'profils/a_propos_public.html'
        context['profil'] = get_or_none(Profil, user=user)
        context['experience'] = get_or_none(Experience, user=user)
        # Ajoutez les données spécifiques à l'entreprise au besoin
    elif user.rôle == 'ecole':
        template_name = 'profils/a_propos_public.html'
        context['profil'] = get_or_none(Profil, user=user)
        context['experience'] = get_or_none(Experience, user=user)
        context['formation'] = get_or_none(Formation, user=user)
        # Ajoutez les données spécifiques à l'école au besoin
    else:
        # Gérer le cas où le rôle n'est pas reconnu
        template_name = 'profils/a_propos_public.html'
    
    return render(request, template_name, context)

''' =========== Paramétres ========= '''
def Settings_profil(request):
    CustomUser = request.user
    return render(request, 'parameter/links.html', {'CustomUser': CustomUser})

def settingEmail(request):
    if request.method == 'POST':
        form = EmailChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            logout(request)
            return redirect('login')
    else:
        form = EmailChangeForm(instance=request.user)
    
    return render(request, 'parameter/updates/email.html', {'form': form})

def settingNames(request):
    if request.method == 'POST':
        form = NameChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            user_role = request.user.rôle
            if user_role == 'admin':
                return redirect('Ad_profile')
            elif user_role == 'professionnel':
                return redirect('Per_profile')
            elif user_role == 'ecole':
                return redirect('Ec_profile')
            elif user_role == 'entreprise':
                return redirect('En_profile')
    else:
        form = NameChangeForm(instance=request.user)
    
    return render(request, 'parameter/updates/names.html', {'form': form, 'CustomUser': request.user})

def settingRole(request):
    if request.method == 'POST':
        form = RoleChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            update_session_auth_hash(request, user)
            return redirect('logout')  # Redirection vers la déconnexion après le changement de rôle
    else:
        form = RoleChangeForm(instance=request.user)
    
    return render(request, 'parameter/updates/role.html', {'form': form})

def settingPassWord(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Met à jour le hachage du mot de passe dans la session
            logout(request)  # Déconnecte l'utilisateur
            return redirect('login')  # Redirige vers la page de connexion après modification du mot de passe
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'parameter/updates/password.html', {'form': form})

def settingDelete(request):
    if request.method == 'POST':
        form = AccountDeleteForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = request.user
            if user.check_password(password):
                user.delete()
                return redirect('login')  # Rediriger vers la page de connexion après suppression du compte
            else:
                form.add_error('password', "Mot de passe incorrect.")
    else:
        form = AccountDeleteForm()
    
    return render(request, 'parameter/updates/delete.html', {'form': form})