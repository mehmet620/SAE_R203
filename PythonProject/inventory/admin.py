from django.contrib import admin
from .models import TypeServeur, Serveur, Utilisateur, Service, Application, UsageRessource


@admin.register(TypeServeur)
class TypeServeurAdmin(admin.ModelAdmin):
    list_display  = ['type', 'description']
    search_fields = ['type']


@admin.register(Serveur)
class ServeurAdmin(admin.ModelAdmin):
    list_display  = ['nom', 'type_serveur', 'nombre_processeur', 'capacite_memoire', 'capacite_stockage']
    list_filter   = ['type_serveur']
    search_fields = ['nom']


@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display  = ['nom', 'prenom', 'email']
    search_fields = ['email', 'nom', 'prenom']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display  = ['nom_service', 'serveur', 'espace_memoire_utilise', 'memoire_vive_necessaire', 'date_lancement']
    list_filter   = ['serveur']
    search_fields = ['nom_service']


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display  = ['nom_application', 'utilisateur']
    search_fields = ['nom_application']


@admin.register(UsageRessource)
class UsageRessourceAdmin(admin.ModelAdmin):
    list_display = ['application', 'service']
    list_filter  = ['application', 'service']
