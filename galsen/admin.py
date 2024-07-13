from django.contrib import admin
from .models import CustomUser
from .models import Profil
from .models import Experience
from .models import Formation
from .models import Post
from .models import MediasPost
from .models import Commentaire
from .models import Share
from .models import Reponse
from .models import Boutique
from .models import Product
from .models import MediasProduct
from .models import Job
from .models import ShareJob
from .models import Notification
from .models import Commande
from .models import ReponseCommande

# Register your models here.

class AdminCustomUser(admin.ModelAdmin):
    list_display = ('username', 'rôle', 'genre', 'email')
admin.site.register(CustomUser, AdminCustomUser)

class AdminProfil(admin.ModelAdmin):
    list_display = ('user', 'description')
admin.site.register(Profil, AdminProfil)

class AdminExperience(admin.ModelAdmin):
    list_display = ('user', 'title')
admin.site.register(Experience, AdminExperience)

class AdminFormation(admin.ModelAdmin):
    list_display = ('user', 'title')
admin.site.register(Formation, AdminFormation)

admin.site.register(Post)
admin.site.register(MediasPost)
admin.site.register(Commentaire)
admin.site.register(Share)
admin.site.register(Reponse)

class AdminBoutique(admin.ModelAdmin):
    list_display = ('nom_boutique', 'devise_boutique', 'date_creation', 'devise_money')
admin.site.register(Boutique, AdminBoutique)

admin.site.register(Product)
admin.site.register(MediasProduct)

class AdminJob(admin.ModelAdmin):
    list_display = ('user', 'title', 'date_creation_post')
admin.site.register(Job, AdminJob)

admin.site.register(ShareJob)
admin.site.register(Notification)
admin.site.register(Commande)
admin.site.register(ReponseCommande)