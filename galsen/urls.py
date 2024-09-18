from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter

# ========== Authentification ===================
from galsen.views import log_in, register, log_out

# ========== Formulaires Posts ===================
from galsen.views import create_post, create_job, create_product, a_propos

# ========== Profiles ===================
from galsen.views import Per_profile, En_profile, En_job, En_Gestion_Boutique, Ec_profile, Ec_job

# ========== Settings Profil ==================
from galsen.views import Settings_profil, settingEmail, settingNames, settingRole, settingPassWord, settingDelete

# ========== Personnels ===================
from galsen.views import Per_posts, Per_ecole, Per_entreprise, Per_job, Per_boutique, Per_notification, En_notification, Ec_notification
# ========== Entreprises ===================
from galsen.views import En_posts, En_personnel, En_ecole, En_boutique, En_postulant
# ========== Ecoles ===================
from galsen.views import Ec_posts, Ec_personnel, Ec_entreprise, Ec_boutique, Ec_postulant
# ========== Admins ===================
from galsen.views import Ad_posts, Ad_personnel, Ad_ecole, Ad_entreprise, Ad_job, Ad_boutique

# ========== Details: Personnels, Entreprise, Ecole ===================
from galsen.views import PersonnelDetails, EcoleDetails, EntrepriseDetails, update_post, update_job

# ========== Update Statu: Personnels, Entreprise, Ecole ===================
from galsen.views import update, update_profile, update_banner, profile, boutique, update_logo_boutique, update_banner_boutique, update_description_boutique, gestion_boutique, rapport_product, les_commandes, update_cv_profil, create_cv_experience, update_cv_experience, create_cv_formation, update_cv_formation, vos_commande, vos_postule, members, amis

# ========== Les Commentaires: Post et Les Réponses:Commentaires ===================
from galsen.views import post_comments, comment_responses

# ========== Les Followers: Les Likes, Les Postules, Les Commandes, postulants ===================
from galsen.views import  AddDislike, AddLikes, post_likes, AddPostule, AddDisPostule
# , RemoveFollower, SharedPosteVue, sharePoste, AddFollower

from . import views

from galsen.views import post_detail, job_detail, jobs_detail, produit_detail, produit_commande, following_view, abonner

router = DefaultRouter()

# Enregistrez vos viewsets avec le routeur
router.register(r'customusers', views.CustomUserViewSet, basename='customuser')
router.register(r'posts', views.PostViewSet, basename='post')
router.register(r'mediasposts', views.MediasPostViewSet, basename='mediaspost')
router.register(r'jobs', views.JobViewSet, basename='job')
router.register(r'boutiques', views.BoutiqueViewSet, basename='boutique')
router.register(r'commentaires', views.CommentaireViewSet, basename='commentaire')
router.register(r'reponses', views.ReponseViewSet, basename='reponse')
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'mediasproducts', views.MediasProductViewSet, basename='mediasproduct')
router.register(r'profils', views.ProfilViewSet, basename='profil')
router.register(r'experiences', views.ExperienceViewSet, basename='experience')
router.register(r'formations', views.FormationViewSet, basename='formation')
router.register(r'notifications', views.NotificationViewSet, basename='notification')
router.register(r'commandes', views.CommandeViewSet, basename='commande')


urlpatterns = [
    
    path('api/', include(router.urls)),
    
    # ========== A Propos ===================
    path('a_propos', a_propos, name = 'a_propos'),
    
    # ========== Les Followers: Les Commentaires ===================
    path('post/<int:post_id>/comments/', post_comments, name='post_comments'),
    path('comment/<int:comment_id>/responses/', comment_responses, name='comment_responses'),
    
    # ========== Les Followers: Les Likes, Les Shares, Suivre, Les postulants ===================
    path('post/<int:pk>/like', AddLikes.as_view(), name='likes'),
    path('post/<int:pk>/dislike', AddDislike.as_view(), name='dislike'),
    path('post/<int:pk>/likes/', post_likes, name='post_likes'),
    path('suivre-utilisateur/<int:user_id>/', views.suivre_utilisateur, name='suivre_utilisateur'),
    path('following/', following_view, name='following_view'),
    path('abonner/', abonner, name='abonner'),
    
    path('abonnement/<int:abonnementId>/', views.abonnementId, name='abonnementId'),
    path('abonner/<int:abonnerId>/', views.abonnerId, name='abonnerId'),
    
    # ========= Postuler à un poste =================
    path('job/<int:pk>/postule', AddPostule.as_view(), name='postule'),
    path('job/<int:pk>/dispostule', AddDisPostule.as_view(), name='dispostule'),
    
    
    # ========== Details: Profil, Personnels, Entreprise, Ecole, Boutique, postes, jobs, Produits, Folowers ===================
    path('personnel/<int:pk>/', PersonnelDetails.as_view(), name='personnel_details'),
    path('ecole/<int:pk>/', EcoleDetails.as_view(), name='ecole_details'),
    path('entreprise/<int:pk>/', EntrepriseDetails.as_view(), name='entreprise_details'),
    path('profiles/<int:pk>/', views.user_detail, name='user_detail'),
    path('a_propos/<int:user_id>/', views.a_propos_detail, name='a_propos_detail'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('job/<int:job_id>/', job_detail, name='job_detail'),
    path('jobs/<int:job_id>/', jobs_detail, name='jobs_detail'),
    path('produit/<int:produit_id>/', produit_detail, name='produit_detail'),
    path('commande/<int:produit_id>/commander', produit_commande, name='produit_commande'),
    path('vos_commande', vos_commande, name='vos_commande'),
    path('vos_postule', vos_postule, name='vos_postule'),
    path('members', members, name='members'),
    path('amis', amis, name='amis'),
     
    # ========== Update Statu, Update Profile, Update Banner, Update Post, Update Job: Personnels, Entreprise, Ecole ===================
    path('update', update, name = 'update'),
    path('update_profile', update_profile, name = 'update_profile'),
    path('update_banner', update_banner, name = 'update_banner'),
    path('update_post/<int:id>/', update_post, name='update_post'),
    path('update_job/<int:job_id>/', update_job, name='update_job'),
    path('update_logo_boutique', update_logo_boutique, name = 'update_logo_boutique'),
    path('update_banner_boutique', update_banner_boutique, name = 'update_banner_boutique'),
    path('update_description_boutique', update_description_boutique, name = 'update_description_boutique'),
    path('gestion_boutique', gestion_boutique, name='gestion_boutique'),
    path('rapport_product', rapport_product, name='rapport_product'),
    path('les_commandes', les_commandes, name='les_commandes'),
    
    path('profil', profile, name = 'profil'),
    path('boutique', boutique, name = 'boutique'),
    
    # ====== CV: Update profile, Create experience, Update experience, Create Formation, Update Formation =====
    path('update_cv_profil', update_cv_profil, name = 'update_cv_profil'),
    
    path('create_cv_experience', create_cv_experience, name = 'create_cv_experience'),
    path('update_cv_experience/<int:experience_id>/', update_cv_experience, name='update_cv_experience'),
    
    path('create_cv_formation', create_cv_formation, name = 'create_cv_formation'),
    path('update_cv_formation/<int:formation_id>/', update_cv_formation, name='update_cv_formation'),

     
    # ========== Authentification ==================
    path('', log_in, name = 'login'),
    path('register', register, name = 'register'),
    path('logout', log_out, name = 'logout'),
    
    
    # =========== reset password ================
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='auth/reset_password.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='auth/reset_password_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='auth/reset.html'), name="password_reset_confirm" ),
    path("reset_password_complete/", auth_views.PasswordResetCompleteView.as_view(template_name='auth/reset_password_complete.html'), name="password_reset_complete"),
    
    # ========== Formulaires Posts ===================
    path('post', create_post, name = 'post'),
    path('job', create_job, name = 'job'),
    path('product', create_product, name = 'product'),
    
    # ========== Supprimer: Posts, Jobs, Product ===================
    path('delete_post/<int:id>/', views.delete_post, name='delete_post'),
    path('delete_job/<int:id>/', views.delete_job, name='delete_job'),
    
    # ========== Profiles ===================
        # ========== Profiles Personnels ===================
    path('per_profile', Per_profile, name = 'Per_profile'),
    
        # ========== Profiles Entreprises ===================
    path('en_profile', En_profile, name = 'En_profile'),
    path('en_job', En_job, name = 'En_job'),
    path('en_Gestion_Boutique', En_Gestion_Boutique, name = 'En_Gestion_Boutique'),
    
            # ========== Profiles Ecole ===================
    path('ec_profile', Ec_profile, name= 'Ec_profile'),
    path('ec_job', Ec_job, name= 'Ec_job'),
    
    # ========== Settings Personnel, Ecole, Entreprise ===================
    path('settings_profil', Settings_profil, name = 'settings_profil'),
    path('settingEmail', settingEmail, name='settingEmail'),
    path('settingNames', settingNames, name='settingNames'),
    path('settingsRole', settingRole, name='settingRole'),
    path('settingPassWord', settingPassWord, name='settingPassWord'),
    path('settingDelete', settingDelete, name='settingDelete'),
    
    # =========== Personnels ================
                # ===== Les Pages =====
    path('per_post', Per_posts, name = 'Per_posts'),
    path('per_ecole', Per_ecole, name = 'Per_ecole'),
    path('per_entreprise', Per_entreprise, name = 'Per_entreprise'),
    path('per_job', Per_job, name = 'Per_job'),
    path('per_boutique', Per_boutique, name = 'Per_boutique'),
    path('per_notification', Per_notification, name = 'Per_notification'),
    
    # =========== Entreprises ================
                # ===== Les Pages =====
    path('en_post', En_posts, name = 'En_posts'),
    path('en_personnel', En_personnel, name = 'En_personnel'),
    path('en_ecole', En_ecole, name = 'En_ecole'),
    path('en_boutique', En_boutique, name = 'En_boutique'),
    path('en_notification', En_notification, name = 'En_notification'),
    path('en_postulant', En_postulant, name='En_postulant'),
    
        # =========== Ecoles ================
                # ===== Les Pages =====
    path('ec_post', Ec_posts, name = 'Ec_posts'),
    path('ec_personnel', Ec_personnel, name = 'Ec_personnel'),
    path('ec_entreprise', Ec_entreprise, name = 'Ec_entreprise'),
    path('ec_boutique', Ec_boutique, name = 'Ec_boutique'),
    path('ec_notification', Ec_notification, name = 'Ec_notification'),
    path('ec_postulant', Ec_postulant, name='Ec_postulant'),
    
    # =========== Admins ================
                # ===== Les Pages =====
    path('ad_post', Ad_posts, name = 'Ad_posts'),
    path('ad_personnel', Ad_personnel, name = 'Ad_Personnel'),
    path('ad_ecole', Ad_ecole, name = 'Ad_ecole'),
    path('ad_entreprise', Ad_entreprise, name = 'Ad_entreprise'),
    path('ad_job', Ad_job, name = 'Ad_job'),
    path('ad_boutique', Ad_boutique, name = 'Ad_boutique'),
]

urlpatterns += router.urls