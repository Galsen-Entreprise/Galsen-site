from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from . import views

# ========== Authentification ===================
from galsen.views import log_in, register, log_out, profile, login_admin

# ========== Les Pages ==================
from galsen.views import home, professionnel, entreprise, ecole, annonce, emplois, boutique

# ========== Section Admin ==================
from galsen.views import SuperAdmin, adminadmin, adminprofessionnel, adminentreprise, adminecole, adminusers, change_user, delete_user

# ========== Formulaires ===================
from galsen.views import create_post, create_job, create_annonce, AddPostule, create_boutique, create_product, facture

# ====== CV: Update profile, Create experience, Update experience, Create Formation, Update Formation =====
from galsen.views import update, update_profile, update_banner, a_propos, update_cv_profil, create_cv_experience, update_cv_experience, create_cv_formation, update_cv_formation

# ========== Les Updates ==================
from galsen.views import update_logo_boutique, update_banner_boutique, update_description_boutique, update_post, update_annonce, update_job, update_product

# ========== Les Followers: Les Likes, Les Postules, Les Commandes, postulants ===================
from galsen.views import AddLikes, following_view, abonner

# ========== Details ===================
from galsen.views import detail_profile, annonce_detail, job_detail, En_Gestion_Boutique, postulant, mon_job, mon_job_detail, mon_annonce, mon_annonce_detail, vos_postule, vos_commande, les_commandes, amis, post_detail, post_comments, comment_responses, produit_commande

# ========== Les Paramétres ==================
from galsen.views import Settings_profil, settingEmail, settingNames, settingRole, settingPassWord, settingDelete

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
router.register(r'facture', views.FactureViewSet, basename='facture')
router.register(r'annonce', views.AnnonceViewSet, basename='annonce')

urlpatterns = [
    
    path('api/', include(router.urls)),
    
    # ========== Authentification ==================
    path('', log_in, name = 'login'),
    path('register', register, name = 'register'),
    path('logout', log_out, name = 'logout'),
    path('profil', profile, name = 'profil'),
    path('login_admin', login_admin, name='login_admin'),
    
    
    # =========== reset password ================
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='auth/reset_password.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='auth/reset_password_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='auth/reset.html'), name="password_reset_confirm" ),
    path("reset_password_complete/", auth_views.PasswordResetCompleteView.as_view(template_name='auth/reset_password_complete.html'), name="password_reset_complete"),
    
    # ========== Les Pages ==================
    path('home', home, name='home'),
    path('professionnel', professionnel, name='professionnel'),
    path('entreprise', entreprise, name='entreprise'),
    path('ecole', ecole, name='ecole'),
    path('annonce', annonce, name='annonce'),
    path('emplois', emplois, name='emplois'),
    path('boutique', boutique, name='boutique'),
    
    # ========== Section Admin ==================
    path('SuperAdmin', SuperAdmin, name= 'SuperAdmin'),
    path('adminadmin', adminadmin, name='adminadmin'),
    path('adminprofessionnel', adminprofessionnel, name='adminprofessionnel'),
    path('adminentreprise', adminentreprise, name='adminentreprise'),
    path('adminecole', adminecole, name='adminecole'),
    path('adminusers', adminusers, name='adminusers'),
    path('change_user/<int:user_id>/', views.change_user, name='change_user'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    
    # ========== Les Formulaires ==================
    path('post', create_post, name = 'post'),
    path('job', create_job, name = 'job'),
    path('create_annonce', create_annonce, name = 'create_annonce'),
    path('job/<int:pk>/postule', AddPostule.as_view(), name='postule'),
    path('create_boutique', create_boutique, name = 'create_boutique'),
    path('product', create_product, name = 'product'),
    path('facture', facture, name='facture'),
    
    # ====== CV: Update profile, Create experience, Update experience, Create Formation, Update Formation =====
    path('a_propos', a_propos, name = 'a_propos'),
    path('update_cv_profil', update_cv_profil, name = 'update_cv_profil'),
    
    path('create_cv_experience', create_cv_experience, name = 'create_cv_experience'),
    path('update_cv_experience/<int:experience_id>/', update_cv_experience, name='update_cv_experience'),
    
    path('create_cv_formation', create_cv_formation, name = 'create_cv_formation'),
    path('update_cv_formation/<int:formation_id>/', update_cv_formation, name='update_cv_formation'),
    
    # ========== Les Updates ==================
    path('update_profile', update_profile, name = 'update_profile'),
    path('update_banner', update_banner, name = 'update_banner'),
    path('update', update, name = 'update'),
    path('update_logo_boutique', update_logo_boutique, name = 'update_logo_boutique'),
    path('update_banner_boutique', update_banner_boutique, name = 'update_banner_boutique'),
    path('update_description_boutique', update_description_boutique, name = 'update_description_boutique'),
    path('update_post/<int:id>/', update_post, name='update_post'),
    path('update_annonce/<int:annonce_id>/', update_annonce, name='update_annonce'),
    path('update_job/<int:job_id>/', update_job, name='update_job'),
    path('update_product/<int:id>/', update_product, name='update_product'),
    
    # ========== Supprimer: Posts, Jobs, Product ===================
    path('delete_post/<int:id>/', views.delete_post, name='delete_post'),
    path('delete_product/<int:id>/', views.delete_product, name='delete_product'),
    path('delete_job/<int:id>/', views.delete_job, name='delete_job'),
    path('delete_annonce/<int:id>/', views.delete_annonce, name='delete_annonce'),
    
    # ========== Les Followers: Les Likes, Les Shares, Suivre ===================
    path('post/<int:pk>/like', AddLikes.as_view(), name='likes'),
    path('suivre-utilisateur/<int:user_id>/', views.suivre_utilisateur, name='suivre_utilisateur'),
    path('following/', following_view, name='following_view'),
    path('abonner/', abonner, name='abonner'),
    
    path('abonnement/<int:abonnementId>/', views.abonnementId, name='abonnementId'),
    path('abonner/<int:abonnerId>/', views.abonnerId, name='abonnerId'),
    
    # ========== Les Détails(Mon Profil, Profil Public, Post, Emplois, Boutique, Postulant) ==================
    path('detail_profile', detail_profile, name= 'detail_profile'),
    path('profiles/<int:user_id>/', views.user_detail, name='user_detail'),
    path('annonce/<int:annonce_id>/', annonce_detail, name='annonce_detail'),
    path('job/<int:job_id>/', job_detail, name='job_detail'),
    path('en_Gestion_Boutique', En_Gestion_Boutique, name = 'En_Gestion_Boutique'),
    path('postulant', postulant, name='postulant'),
    path('vos_postule', vos_postule, name='vos_postule'),
    path('mon_job', mon_job, name='mon_job'),
    path('mon_annonce', mon_annonce, name='mon_annonce'),
    path('mon_job/<int:job_id>/', mon_job_detail, name='mon_job_detail'),
    path('mon_annonce/<int:annonce_id>/', mon_annonce_detail, name='mon_annonce_detail'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('vos_commande', vos_commande, name='vos_commande'),
    path('les_commandes', les_commandes, name='les_commandes'),
    path('amis', amis, name='amis'),
    path('a_propos/<int:user_id>/', views.a_propos_detail, name='a_propos_detail'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('post/<int:post_id>/comments/', post_comments, name='post_comments'),
    path('comment/<int:comment_id>/responses/', comment_responses, name='comment_responses'),
    path('categorie/<str:category>/', views.categorie_view, name='categorie'),
    path('commande/<int:produit_id>/commander', produit_commande, name='produit_commande'),
    path('boutique/<int:boutique_id>/', views.boutique_detail, name='boutique_detail'),
    
    # ========== Les Paramétres ==================
    path('settings_profil', Settings_profil, name = 'settings_profil'),
    path('settingEmail', settingEmail, name='settingEmail'),
    path('settingNames', settingNames, name='settingNames'),
    path('settingsRole', settingRole, name='settingRole'),
    path('settingPassWord', settingPassWord, name='settingPassWord'),
    path('settingDelete', settingDelete, name='settingDelete'),
]

urlpatterns += router.urls