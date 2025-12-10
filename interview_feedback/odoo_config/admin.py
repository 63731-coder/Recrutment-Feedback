from django.contrib import admin
from django.contrib import messages # Important pour afficher les alertes (vert/rouge)
from .models import OdooConfig


class OdooConfigAdmin(admin.ModelAdmin):
    # 1. On affiche les colonnes utiles dans la liste
    list_display = ('url', 'username', 'db')
    
    # 2. On déclare notre nouvelle action dans le menu déroulant
    actions = ['action_tester_connexion']

    # 3. On définit ce que fait l'action
    @admin.action(description='Tester la connexion Odoo')
    def action_tester_connexion(self, request, queryset):
        # Pour chaque configuration sélectionnée (cochée)
        for config in queryset:
            # On appelle notre "moteur" (la méthode du modèle)
            resultat = config.test_connection()
            
            # On affiche le résultat à l'utilisateur
            if "Succès" in resultat:
                self.message_user(request, resultat, level=messages.SUCCESS)
            else:
                self.message_user(request, resultat, level=messages.ERROR)

# 4. On enregistre le modèle AVEC cette configuration spéciale
admin.site.register(OdooConfig, OdooConfigAdmin)