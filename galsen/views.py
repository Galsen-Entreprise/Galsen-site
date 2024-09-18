from django.http import HttpResponse
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
import os
import time
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from django.core.exceptions import ValidationError
from django.contrib import messages
from .decorators import role_required

from .models import CustomUser, Post, MediasPost, Job, Boutique, Commentaire, Reponse, Product, MediasProduct, Profil, Experience, Formation, Notification, Commande
from .serializers import CustomUserSerializer, PostSerializer, MediasPostSerializer, JobSerializer, BoutiqueSerializer, CommentaireSerializer, ReponseSerializer, ProductSerializer, MediasProductSerializer, ProfilSerializer, ExperienceSerializer, FormationSerializer, NotificationSerializer, CommandeSerializer
from django.views.generic import DetailView, View
from galsen.utils import obtenir_marque_dispositif
from django.http import JsonResponse
from django.db.models import Q
from django.core.mail import send_mail
from django.utils.translation import activate
from django.contrib.auth import get_user_model

from rest_framework import viewsets
from .serializers import CustomUserSerializer
from .forms import EmailChangeForm, NameChangeForm, RoleChangeForm, AccountDeleteForm, PasswordChangeForm


# Les APi
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

def vos_commande(request):
    # Récupérer les commandes de l'utilisateur connecté
    commandes = Commande.objects.filter(user=request.user)
    
    context = {
        'commandes': commandes,
    }
    
    return render(request, 'Commandes/Vos_commandes.html', context)

def vos_postule(request):
    # Récupérer les postulations de l'utilisateur connecté
    postulations = Job.objects.filter(postule_job=request.user)
    
    context = {
        'postulations': postulations,
    }
    
    return render(request, 'Commandes/Vos_postules.html', context)

def members(request):
    user_role = request.user.rôle
    
    # Récupérer tous les utilisateurs ayant le même rôle que l'utilisateur connecté
    users = CustomUser.objects.filter(rôle=user_role).exclude(id=request.user.id)

    # Récupérer la valeur du champ de recherche
    search_query = request.GET.get('poste', '')

    # Si une recherche est effectuée, filtrer les utilisateurs par établissement, prénom ou nom
    if search_query:
        # Rechercher dans le prénom, le nom ou l'établissement
        users = users.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(etablissement__icontains=search_query)
        )
    
    context = {
        'users': users,
        'search_query': search_query,  # Passer la recherche pour réutilisation
    }
    
    return render(request, 'profiles/members/member.html', context)

def amis(request):
    # Récupérer l'utilisateur connecté
    current_user = request.user

    # Récupérer ceux que l'utilisateur suit et ceux qui le suivent
    following = current_user.get_following()
    followers = current_user.get_followers()

    # Trouver les amis mutuels (ceux que l'utilisateur suit et qui le suivent)
    mutual_friends = set(following).intersection(set(followers))

    # Récupérer la valeur du champ de recherche
    search_query = request.GET.get('search', '')

    if search_query:
        # Appliquer le filtre sur les utilisateurs suivis (following)
        following = following.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(etablissement__icontains=search_query)
        )

        # Appliquer le filtre sur les utilisateurs qui suivent l'utilisateur (followers)
        followers = followers.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(etablissement__icontains=search_query)
        )

        # Filtrer les amis mutuels manuellement (car intersection() convertit en set)
        mutual_friends = [friend for friend in mutual_friends if
                          search_query.lower() in friend.first_name.lower() or
                          search_query.lower() in friend.last_name.lower() or
                          search_query.lower() in (friend.etablissement or '').lower()]

    context = {
        'following': following,
        'followers': followers,
        'mutual_friends': mutual_friends,
        'search_query': search_query,
    }

    return render(request, 'profiles/amis/amis.html', context)



def my_view(request):
    user_language = get_user_model().objects.get(pk=request.user.pk).langue
    activate(user_language)

# ========== Details: profil, A propos ===================
def user_detail(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    context = {}
    
    if user.rôle == 'personnel':
        template_name = 'profiles/id/personnel.html'
        context['personnel'] = user
    elif user.rôle == 'entreprise':
        template_name = 'profiles/id/entreprise.html'
        context['entreprise'] = user
    elif user.rôle == 'ecole':
        template_name = 'profiles/id/ecole.html'
        context['ecole'] = user
    
    # Ajouter le nombre total de likes reçus dans le contexte
    context['total_likes_received'] = user.total_likes_received()

    return render(request, template_name, context)

# break

def abonnementId(request, abonnementId):
    # Récupérez l'utilisateur par son ID d'abonnement
    utilisateur = get_object_or_404(CustomUser, id=abonnementId)
    
    # Récupérez la liste des utilisateurs suivis par l'utilisateur spécifique
    following_users = utilisateur.following_users.all()  # Assurez-vous que following_users est correctement défini dans votre modèle
    
    context = {
        'utilisateur': utilisateur,
        'following_users': following_users,
    }
    
    return render(request, 'Details/id/abonnement.html', context)

def abonnerId(request, abonnerId):
    # Récupérez l'utilisateur par son ID d'abonnement
    utilisateur = get_object_or_404(CustomUser, id=abonnerId)
    
    # Récupérez la liste des abonnés de l'utilisateur spécifique
    abonnes = utilisateur.followers.all()  # Assurez-vous que abonnes est correctement défini dans votre modèle
    
    context = {
        'utilisateur': utilisateur,
        'abonnes': abonnes,
    }
    
    return render(request, 'Details/id/abonner.html', context)

def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None

def a_propos_detail(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    context = {'user': user}
    
    if user.rôle == 'personnel':
        template_name = 'profiles/id/A_propos/cv_personnel.html'
        context['profil'] = get_or_none(Profil, user=user)
        context['experience'] = get_or_none(Experience, user=user)
        context['formation'] = get_or_none(Formation, user=user)
    elif user.rôle == 'entreprise':
        template_name = 'profiles/id/A_propos/propos_entreprise.html'
        context['profil'] = get_or_none(Profil, user=user)
        context['experience'] = get_or_none(Experience, user=user)
        # Ajoutez les données spécifiques à l'entreprise au besoin
    elif user.rôle == 'ecole':
        template_name = 'profiles/id/A_propos/propos_ecole.html'
        context['profil'] = get_or_none(Profil, user=user)
        context['experience'] = get_or_none(Experience, user=user)
        context['formation'] = get_or_none(Formation, user=user)
        # Ajoutez les données spécifiques à l'école au besoin
    else:
        # Gérer le cas où le rôle n'est pas reconnu
        template_name = 'profiles/id/A_propos/default.html'
    
    return render(request, template_name, context)
    
# ========== Details: personnels ===================
class PersonnelDetails(DetailView):
    model = CustomUser
    template_name = 'profiles/id/personnel.html'
    context_object_name = 'personnel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        personnel = self.get_object()
        context['total_likes_received'] = personnel.total_likes_received()
        print("Contexte de la vue détaillée :", context)
        return context
# break   

# ========== Details: Ecole ===================
class EcoleDetails(DetailView):
    model = CustomUser
    template_name = 'profiles/id/ecole.html'
    context_object_name = 'ecole'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ecole = self.get_object()
        context['total_likes_received'] = ecole.total_likes_received()
        print("Contexte de la vue détaillée :", context)
        return context  
    
# ========== Details: Entreprise ===================
class EntrepriseDetails(DetailView):
    model = CustomUser
    template_name = 'profiles/id/entreprise.html'
    context_object_name = 'entreprise'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entreprise = self.get_object()
        context['total_likes_received'] = entreprise.total_likes_received()
        print("Contexte de la vue détaillée :", context)
        return context 

# ========= Details Postes, Jobs, Boutique ===========
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'Details/post.html', {'post': post})

def job_detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    return render(request, 'Details/job.html', {'job': job})

def jobs_detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    return render(request, 'Details/mon_job.html', {'job': job})

def produit_detail(request, produit_id):
    produit = get_object_or_404(Product, pk=produit_id)
    
    return render(request, 'Commandes/commande.html', {'produit': produit})

def produit_commande(request, produit_id):
    produit = get_object_or_404(Product, pk=produit_id)
    commande = request.POST.get('commande')
    precision = request.POST.get('precision')
    
    commander = Commande.objects.create(product=produit, user=request.user, commande=commande, precision=precision)
    
    user_role = request.user.rôle  
    if user_role == 'admin':
        return redirect('Ad_boutique')
    elif user_role == 'personnel':
        return redirect('Per_boutique')
    elif user_role == 'ecole':
        return redirect('Ec_boutique')
    elif user_role == 'entreprise':
        return redirect('En_boutique')
  
    produit = get_object_or_404(Product, pk=produit_id)
    commandes = Commande.objects.filter(produit=produit)
    return render(request, 'Commandes/commande.html', {'produit': produit, 'commandes': commandes})

# ========== Modifier: Post, job ===================
def update_post(request, id):
    post = get_object_or_404(Post, id=id)
    medias_post = MediasPost.objects.filter(post=post).first()

    if request.method == 'POST':
        post.contenu_post = request.POST['contenu_post']
        post.tag_post = request.POST['tag_post']
        post.save()

        new_image_file = request.FILES.get('image')
        new_video_file = request.FILES.get('video')

        if medias_post and medias_post.image and os.path.exists(medias_post.image.path):
            medias_post.image.delete(save=False)

        if post.video and os.path.exists(post.video.path):
            post.video.delete(save=False)

        if new_video_file:
            post.video = new_video_file
        post.save()

        if medias_post:
            if new_image_file:
                medias_post.image = new_image_file
            medias_post.save()
        else:
            if new_image_file:
                MediasPost.objects.create(post=post, image=new_image_file)

        user_role = request.user.rôle  
        if user_role == 'admin':
            return redirect('Ad_profile')
        elif user_role == 'personnel':
            return redirect('Per_profile')
        elif user_role == 'ecole':
            return redirect('Ec_profile')
        elif user_role == 'entreprise':
            return redirect('En_profile')

    return render(request, 'formulaires/update/update_post.html', {'post': post, 'medias_post': medias_post})


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
        elif user_role == 'personnel':
            return redirect('Per_profile')
        elif user_role == 'ecole':
            return redirect('Ec_profile')
        elif user_role == 'entreprise':
            return redirect('En_profile')
        
    # Charger les données de l'expérience dans le formulaire
    context = {'job': job}
        
    return render(request, 'formulaires/update/update_job.html', context)

# ========== Supprimer: Post, Job ===================
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
    elif user_role == 'personnel':
        return redirect('Per_profile')
    elif user_role == 'ecole':
        return redirect('Ec_profile')
    elif user_role == 'entreprise':
        return redirect('En_profile')


def delete_job(request, id):
    job = get_object_or_404(Job, id=id)

    job.delete()

    user_role = request.user.rôle
    if user_role == 'admin':
        return redirect('Ad_profile')
    elif user_role == 'personnel':
        return redirect('Per_profile')
    elif user_role == 'ecole':
        return redirect('Ec_profile')
    elif user_role == 'entreprise':
        return redirect('En_profile')

# Create your views here.
''' =========== Authentication ========= '''
def log_in(request):
    if request.method == 'POST':
        email = request.POST['email']  
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)
        if user is not None and user.is_authenticated:
            login(request, user)

            roles_valides = ['admin','personnel', 'ecole', 'entreprise']

            if user.rôle == 'admin':
                # messages.error(request, "Vous n'avez pas la permission d'accéder à cette page.")
                return redirect('Ad_posts')
            elif user.rôle in roles_valides:
                if user.rôle == 'personnel':
                    return redirect('Per_posts')
                elif user.rôle == 'ecole':
                    return redirect('Ec_posts')
                elif user.rôle == 'entreprise':
                    return redirect('En_posts')
            else:
                messages.error(request, "Vous n'avez pas la permission d'accéder à cette page.")

    return render(request, 'auth/login.html')

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
            elif user_role == 'personnel':
                return render(request, 'auth/personnel.html')
            elif user_role == 'ecole':
                return render(request, 'auth/ecole.html')
            elif user_role == 'entreprise':
                return render(request, 'auth/entreprise.html')
    else:
        form = CustomUserCreationForm()

    return render(request, 'auth/register.html', {'form': form})

def profile(request):
    if request.method == 'POST':
        user = request.user
        
        # Récupérer les données du formulaire POST
        pays = request.POST.get('pays')
        ville = request.POST.get('ville')
        quartier = request.POST.get('quartier')
        indicatif = request.POST.get('indicatif')
        phone = request.POST.get('phone')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        birthday = request.POST.get('birthday')

        # Mettre à jour les champs appropriés
        user.pays = pays
        user.ville = ville
        user.quartier = quartier
        user.indicatif_pays = indicatif
        user.number_phone = phone

        # Vérifier si les champs first_name et last_name sont fournis, sinon les définir sur None
        user.first_name = firstname if firstname else None
        user.last_name = lastname if lastname else None

        user.birthday = birthday

        user.save()

        messages.success(request, 'Profil mis à jour avec succès.')

        return redirect('login')

    user_role = request.user.rôle

    if user_role == 'admin':
        return render(request, '')
    elif user_role == 'personnel':
        return render(request, 'auth/personnel.html')
    elif user_role == 'ecole':
        return render(request, 'auth/ecole.html')
    elif user_role == 'entreprise':
        return render(request, 'auth/entreprise.html')


def log_out(request):
    # pass
    logout(request)
    messages.success(request, 'Déconnecter👌🏾')
    return redirect('login')

# ========== Formulaires Posts ===================
@role_required(['admin','personnel', 'ecole', 'entreprise'])
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
        elif user_role == 'personnel':
            return redirect('Per_posts')
        elif user_role == 'ecole':
            return redirect('Ec_posts')
        elif user_role == 'entreprise':
            return redirect('En_posts')
    
    return render(request, 'formulaires/post.html')



@role_required(['admin','personnel', 'ecole', 'entreprise'])
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
        elif user_role == 'personnel':
            return redirect('Per_posts')
        elif user_role == 'ecole':
            return redirect('Ec_posts')
        elif user_role == 'entreprise':
            return redirect('En_posts')
        
    return render(request, 'formulaires/job.html')

@role_required(['admin','personnel', 'ecole', 'entreprise'])
def create_product(request):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        description = request.POST.get('description')
        nom_produit = request.POST.get('nom_produit')
        prix = request.POST.get('prix')
        video = request.FILES.get('video')
        # Récupérer les fichiers images envoyés
        images = request.FILES.getlist('image')
        
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
            video=video
        )
        
        # Si une image est fournie, créer un objet MediasProduct correspondant
       # Itérer sur chaque image et les enregistrer dans la base de données
        for image in images:
            MediasProduct.objects.create(
                produit=new_product,
                image=image
            )
        
        # Rediriger l'utilisateur vers une autre page après la création du produit
        return redirect('En_Gestion_Boutique')
        
    return render(request, 'formulaires/product.html')

@role_required(['admin','personnel', 'ecole', 'entreprise'])
def update(request):
    user_role = request.user.rôle

    if user_role == 'entreprise':
        # Charger le modèle de mise à jour pour l'entreprise
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

            # Rediriger vers le profil de l'entreprise
            return redirect('En_profile')

        # Charger le modèle de mise à jour pour l'entreprise
        return render(request, 'formulaires/update/admin_statut.html')
    
    elif user_role == 'personnel':
        # Charger le modèle de mise à jour pour le personnel
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
            return redirect('Per_profile')
        
        return render(request, 'formulaires/update/personnel_statut.html')

    elif user_role == 'ecole':
        # Charger le modèle de mise à jour pour l'école
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
            
            return redirect('Ec_profile')
        
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

@role_required(['admin','personnel', 'ecole', 'entreprise'])
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
    if user_role == 'personnel':
        return render(request, 'profiles/A_Propos/cv_personnel.html', {'user': user, 'profil': profil, 'experience': experience, 'formation': formation})
    elif user_role == 'ecole':
        return render(request, 'profiles/A_Propos/propos_ecole.html', {'user': user, 'profil': profil, 'experience': experience, 'formation': formation})
    elif user_role == 'entreprise':
        return render(request, 'profiles/A_Propos/propos_entreprise.html', {'user': user, 'profil': profil, 'experience': experience, 'formation': formation})

@role_required(['admin','personnel', 'ecole', 'entreprise'])
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
        elif user_role == 'personnel':
            return redirect('Per_profile')
        elif user_role == 'ecole':
            return redirect('Ec_profile')
        elif user_role == 'entreprise':
            return redirect('En_profile')
        # Rediriger vers la page de profil appropriée
    else:
        return render(request, 'formulaires/update/update_profile.html', {'CustomUser': CustomUser})
    
# break

# Update logo Boutique
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

# Break
def les_commandes(request):
    # Récupérer toutes les commandes de l'utilisateur connecté
    commandes = Commande.objects.filter(user=request.user)
    
    context = {
        'commandes': commandes,
    }
    
    return render(request, 'profiles/mon_profile/commandes.html', context)

def gestion_boutique(request):
    try:
        # Récupère la boutique associée à l'utilisateur connecté
        user_boutique = Boutique.objects.get(user=request.user)
        
        # Récupérer les produits associés à cette boutique
        produits = user_boutique.product_set.all()
        
    except Boutique.DoesNotExist:
        # Redirige vers la page 'auth/boutique.html' si la boutique n'existe pas
        return render(request, 'auth/boutique.html')

    # Maintenant, tu peux utiliser user_boutique et produits dans ton contexte pour le rendre disponible dans ton template
    context = {
        'user_boutique': user_boutique,
        'produits': produits
    }
    return render(request, 'profiles/mon_profile/gestion_boutique.html', context)
#break


def rapport_product(request):
    try:
        # Récupère la boutique associée à l'utilisateur connecté
        user_boutique = Boutique.objects.get(user=request.user)
        
    except Boutique.DoesNotExist:
        # Redirige vers la page 'auth/boutique.html' si la boutique n'existe pas
        return render(request, 'auth/boutique.html')

    # Maintenant, tu peux utiliser user_boutique et produits dans ton contexte pour le rendre disponible dans ton template
    context = {
        'user_boutique': user_boutique
    }
    return render(request, 'profiles/mon_profile/rapport_product.html', context)
#break

# ====== CV: Update profile, Experience =====
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

@role_required(['admin','personnel', 'ecole', 'entreprise'])
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
        elif user_role == 'personnel':
            return redirect('Per_profile')
        elif user_role == 'ecole':
            return redirect('Ec_profile')
        elif user_role == 'entreprise':
            return redirect('En_profile')
        # Rediriger vers la page de profil ou toute autre page appropriée
    else:
        return render(request, 'formulaires/update/update_banner.html', {'CustomUser': CustomUser})

# ========== Profiles ===================
        # ========== Profiles personnels ===================
@role_required(['personnel'])
def Per_profile(request):
    CustomUser = request.user
    total_likes_received = CustomUser.total_likes_received()
    return render(request, 'profiles/mon_profile/personnel.html', {'CustomUser': CustomUser, 'total_likes_received': total_likes_received})

# ========== Break ===================

        # ========== Profiles Entreprises ===================
@role_required(['entreprise'])
def En_profile(request):
    CustomUser = request.user
    total_likes_received = CustomUser.total_likes_received()
    return render(request, 'profiles/mon_profile/entreprise_post.html', {'CustomUser': CustomUser, 'total_likes_received': total_likes_received})

@role_required(['entreprise'])
def En_job(request):
    CustomUser = request.user
    total_likes_received = CustomUser.total_likes_received()
    return render(request, 'profiles/mon_profile/entreprise_job.html', {'CustomUser': CustomUser, 'total_likes_received': total_likes_received})

@role_required(['entreprise'])
def En_Gestion_Boutique(request):
    try:
        # Récupère la boutique associée à l'utilisateur connecté
        user_boutique = Boutique.objects.get(user=request.user)
        
        # Récupérer les produits associés à cette boutique
        produits = user_boutique.product_set.all()
        
    except Boutique.DoesNotExist:
        # Redirige vers la page 'auth/boutique.html' si la boutique n'existe pas
        return render(request, 'auth/boutique.html')

    # Maintenant, tu peux utiliser user_boutique et produits dans ton contexte pour le rendre disponible dans ton template
    context = {
        'user_boutique': user_boutique,
        'produits': produits
    }
    return render(request, 'profiles/mon_profile/boutique.html', context)
# Break

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
            elif user_role == 'personnel':
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

def boutique(request):
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
# break

        # ========== Profiles Ecole ===================
@role_required(['ecole'])
def Ec_profile(request):
    CustomUser = request.user
    total_likes_received = CustomUser.total_likes_received()
    return render(request, 'profiles/mon_profile/ecole_post.html', {'CustomUser': CustomUser, 'total_likes_received': total_likes_received})

@role_required(['ecole'])
def Ec_job(request):
    CustomUser = request.user
    total_likes_received = CustomUser.total_likes_received()
    return render(request, 'profiles/mon_profile/ecole_job.html', {'CustomUser': CustomUser, 'total_likes_received': total_likes_received})

# ========== Les commentaires: Posts ===================
@role_required(['admin','personnel', 'ecole', 'entreprise'])
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
@role_required(['admin','personnel', 'ecole', 'entreprise'])
def comment_responses(request, comment_id):
    
    if request.method == 'POST':
        comment = get_object_or_404(Commentaire, id=comment_id)
        contenu_text = request.POST.get('contenu_text')
        image = request.FILES.get('image')
        
        reponse = Reponse.objects.create(commentaire=comment, user=request.user, contenu_text=contenu_text, image=image)
    
    comment = get_object_or_404(Commentaire, id=comment_id)
    responses = Reponse.objects.filter(commentaire_id=comment.id)
    return render(request, 'Commentaire/response.html', {'comment': comment, 'responses': responses})

# ========== Les Followers: Les Likes, Les Dislikes, Les Shares, LEs Commandes ===================
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
        elif user_role == 'personnel':
            return redirect('Per_job')
        elif user_role == 'ecole':
            return redirect('Ec_job')
        elif user_role == 'entreprise':
            return redirect('En_job')

       
class AddFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = get_object_or_404(CustomUser, pk=pk)
        profile.followers.add(request.user)
        return JsonResponse({'success': True})

class RemoveFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = get_object_or_404(CustomUser, pk=pk)
        profile.followers.remove(request.user)
        return JsonResponse({'success': True})

class AddDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)

        # Vérifier si l'utilisateur a déjà aimé ou n'aime pas le poste
        is_like = post.like_post.filter(pk=request.user.pk).exists()
        is_dislike = post.dislike.filter(pk=request.user.pk).exists()

        # Si l'utilisateur a déjà aimé le poste, le retirer de la liste des likes
        if is_like:
            post.like_post.remove(request.user)

        # Si l'utilisateur n'a pas déjà détesté le poste, l'ajouter aux dislikes
        if not is_dislike:
            post.dislike.add(request.user)
            dislike_icon = '<i class="fa fa-thumbs-down primary"></i>'
        # Si l'utilisateur a déjà détesté le poste, le retirer des dislikes
        else:
            post.dislike.remove(request.user)
            dislike_icon = '<i class="fa fa-thumbs-down"></i>'

        # Renvoyer les informations mises à jour
        response_data = {
            'dislike_count': post.dislike.count(),
            'dislike_icon': dislike_icon,
        }
        
        # Retourner une réponse JSON

class AddDisPostule(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        job = get_object_or_404(Job, pk=pk)

        # Vérifier si l'utilisateur a déjà aimé ou n'aime pas le poste
        is_postule = job.postule_job.filter(pk=request.user.pk).exists()
        is_dispostule = job.dispostule.filter(pk=request.user.pk).exists()

        # Si l'utilisateur a déjà aimé le poste, le retirer de la liste des likes
        if is_postule:
            job.postule_job.remove(request.user)

        # Si l'utilisateur n'a pas déjà détesté le poste, l'ajouter aux dislikes
        if not is_dispostule:
            job.dispostule.add(request.user)
            dispostule_icon = '<i class="fa fa-thumbs-down primary"></i>'
        # Si l'utilisateur a déjà détesté le poste, le retirer des dislikes
        else:
            job.dispostule.remove(request.user)
            dispostule_icon = '<i class="fa fa-thumbs-down"></i>'

        # Renvoyer les informations mises à jour
        response_data = {
            'dispostule_count': job.dispostule.count(),
            'dispostule_icon': dispostule_icon,
        }


def post_likes(request, pk):
    # Récupérer l'instance du poste
    post = get_object_or_404(Post, pk=pk)

    # Récupérer les utilisateurs qui ont aimé ce poste
    users_liking_post = post.like_post.all()

    context = {
        'post': post,
        'users_liking_post': users_liking_post,
    }

    return render(request, 'Details/likes.html', context)

# Details ABONNEMENT
def following_view(request):
    user = request.user
    following_users = user.get_following()
    return render(request, 'Details/abonnement.html', {'following_users': following_users})

# DETAILS ABONNES
def abonner(request):
    # Récupérer l'utilisateur actuel
    user = request.user
    # Récupérer la liste des abonnés de l'utilisateur actuel
    abonnes = user.get_followers()
    return render(request, 'Details/abonner.html', {'abonnes': abonnes})

   
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

''' =========== personnels ========= '''
@role_required(['personnel'])
def Per_posts(request):
    posts = Post.objects.select_related('user').prefetch_related('mediaspost_set').order_by('-date_creation_post').all()
    
    if request.method == "GET":
        contenu_post = request.GET.get('poste')
        if contenu_post is not None:
            posts = Post.objects.filter(contenu_post__icontains=contenu_post)

    if request.user.is_authenticated:
        marque_dispositif = obtenir_marque_dispositif(request)
        request.user.marque_dispositif = marque_dispositif
        request.user.save()

    if request.user.is_authenticated:
        user_language = request.user.langue
        activate(user_language)

    for post in posts:
        post.is_followed = request.user.is_following(post.user)

    context = {
        'posts': posts,
    }
    return render(request, 'users/Personnel/post.html', context)

@role_required(['personnel'])
def Per_ecole(request):
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
    
    return render(request, 'users/Personnel/ecole.html', context)

@role_required(['personnel'])
def Per_entreprise(request):
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
    
    return render(request, 'users/Personnel/entreprise.html', context)

@role_required(['personnel'])
def Per_job(request):
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
    
    return render(request, 'users/Personnel/job.html', context)

@role_required(['personnel'])
def Per_boutique(request):
    # Récupérer l'utilisateur connecté
    user = request.user

    # Récupérer les produits commandés par l'utilisateur connecté
    produits_commandes = Commande.objects.filter(user=user).values_list('product', flat=True)

    # Récupérer tous les produits disponibles en excluant ceux commandés par l'utilisateur connecté
    produits = Product.objects.select_related('boutique').order_by('-date_creation').exclude(id__in=produits_commandes)

    if request.method == "GET":
        nom_produit = request.GET.get('boutique')
        if nom_produit is not None:
            produits = produits.filter(nom_produit__icontains=nom_produit)

    context = {
        'user': user,
        'produits': produits,
    }

    return render(request, 'users/Personnel/boutique.html', context)

@role_required(['personnel'])
def Per_notification(request):
    return render(request, 'users/Personnel/notification.html')

''' =========== Entreprises ========= '''
@role_required(['entreprise'])
def En_posts(request):
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

    return render(request, 'users/Entreprise/post.html', context)

@role_required(['entreprise'])
def En_personnel(request):
    CustomUsers = CustomUser.objects.filter(rôle='personnel')
    user = request.user
    query = request.GET.get('personnel')

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

        CustomUsers = CustomUser.objects.filter(rôle='personnel').filter(filter_query)

    context = {
        'CustomUsers': CustomUsers,
        'user': user,
        'query': query,  # Ajouter la requête pour la réafficher dans le formulaire
        'result_count': CustomUsers.count()
    }
    
    return render(request, 'users/Entreprise/personnel.html', context)

@role_required(['entreprise'])
def En_ecole(request):
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
    
    return render(request, 'users/Entreprise/ecole.html', context)

@role_required(['entreprise'])
def En_boutique(request):
    # Récupérer l'utilisateur connecté
    user = request.user

    # Récupérer les produits commandés par l'utilisateur connecté
    produits_commandes = Commande.objects.filter(user=user).values_list('product', flat=True)

    # Récupérer tous les produits disponibles en excluant ceux commandés par l'utilisateur connecté
    produits = Product.objects.select_related('boutique').order_by('-date_creation').exclude(id__in=produits_commandes)

    if request.method == "GET":
        nom_produit = request.GET.get('boutique')
        if nom_produit is not None:
            produits = produits.filter(nom_produit__icontains=nom_produit)

    context = {
        'user': user,
        'produits': produits
    }
    return render(request, 'users/Entreprise/boutique.html', context)

@role_required(['entreprise'])
def En_postulant(request):
    # Récupérer toutes les offres postées par l'utilisateur connecté
    user_jobs = Job.objects.filter(user=request.user)  # Assurez-vous que `user` est le champ qui stocke l'utilisateur qui a posté l'offre

    # Récupérer tous les postulants pour les offres de l'utilisateur connecté
    postulants = {}
    for job in user_jobs:
        postulants[job] = job.postule_job.all()

    context = {
        'postulants': postulants,
    }
    
    return render(request, 'users/Entreprise/postulant.html', context)

@role_required(['entreprise'])
def En_notification(request):
    return render(request, 'users/Entreprise/notification.html')

''' =========== Ecoles ========= '''
@role_required(['ecole'])
def Ec_posts(request):
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
    
    return render(request, 'users/Ecole/post.html', context)

@role_required(['ecole'])
def Ec_personnel(request):
    CustomUsers = CustomUser.objects.filter(rôle='personnel')
    user = request.user
    query = request.GET.get('personnel')

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

        CustomUsers = CustomUser.objects.filter(rôle='personnel').filter(filter_query)

    context = {
        'CustomUsers': CustomUsers,
        'user': user,
        'query': query,  # Ajouter la requête pour la réafficher dans le formulaire
        'result_count': CustomUsers.count()
    }

    return render(request, 'users/Ecole/personnel.html', context)

@role_required(['ecole'])
def Ec_entreprise(request):
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
    
    return render(request, 'users/Ecole/entreprise.html', context)

@role_required(['ecole'])
def Ec_boutique(request):
    # Récupérer l'utilisateur connecté
    user = request.user

    # Récupérer les produits commandés par l'utilisateur connecté
    produits_commandes = Commande.objects.filter(user=user).values_list('product', flat=True)

    # Récupérer tous les produits disponibles en excluant ceux commandés par l'utilisateur connecté
    produits = Product.objects.select_related('boutique').order_by('-date_creation').exclude(id__in=produits_commandes)

    if request.method == "GET":
        nom_produit = request.GET.get('boutique')
        if nom_produit is not None:
            produits = produits.filter(nom_produit__icontains=nom_produit)

    context = {
        'user': user,
        'produits': produits
    }
    return render(request, 'users/Ecole/boutique.html', context)

@role_required(['ecole'])
def Ec_notification(request):
    return render(request, 'users/Ecole/notification.html')

@role_required(['ecole'])
def Ec_postulant(request):
    # Récupérer toutes les offres postées par l'utilisateur connecté
    user_jobs = Job.objects.filter(user=request.user)  # Assurez-vous que `user` est le champ qui stocke l'utilisateur qui a posté l'offre

    # Récupérer tous les postulants pour les offres de l'utilisateur connecté
    postulants = {}
    for job in user_jobs:
        postulants[job] = job.postule_job.all()

    context = {
        'postulants': postulants,
    }
    
    return render(request, 'users/Ecole/postulant.html', context)

''' =========== Admins ========= '''
@role_required(['admin'])
def Ad_posts(request):
    # Récupérer tous les posts avec les médias associés, les utilisateurs, et la date de création
    posts = Post.objects.select_related('user').prefetch_related('mediaspost_set').order_by('-date_creation_post').all()
    user = request.user

    context = {
        'posts': posts,
        'user': user
    }
    
    return render(request, 'users/Admin/post.html', context)

@role_required(['admin'])
def Ad_personnel(request):
    user = request.user

    context = {
        'user': user
    }
    
    return render(request, 'users/Admin/personnel.html', context)

@role_required(['admin'])
def Ad_ecole(request):
    user = request.user

    context = {
        'user': user
    }
    
    return render(request, 'users/Admin/ecole.html', context)

@role_required(['admin'])
def Ad_entreprise(request):
    user = request.user

    context = {
        'user': user
    }
    return render(request, 'users/Admin/entreprise.html', context)

@role_required(['admin'])
def Ad_job(request):
    user = request.user

    context = {
        'user': user
    }
    
    return render(request, 'users/Admin/job.html', context)

@role_required(['admin'])
def Ad_boutique(request):
    user = request.user

    context = {
        'user': user
    }
    
    return render(request, 'users/Admin/boutique.html', context)


class PostNotification(View):
    def get(self, request, notification_pk, post_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        post = Post.objects.get(pk=post_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('post-detail', pk=post_pk)
    
class FollowNotification(View):
    def get(self, request, notification_pk, profile_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        profile = CustomUser.objects.get(pk=profile_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('profile', pk=profile_pk)