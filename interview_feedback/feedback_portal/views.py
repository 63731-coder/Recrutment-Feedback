from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import xmlrpc.client
from odoo_config.models import OdooConfig

@login_required
def index(request):
    # 1. On récupère la configuration active
    config = OdooConfig.objects.first()
    
    # Si aucune config n'existe, on évite le crash
    if not config:
        return render(request, 'feedback_portal/error.html', {'message': "Pas de configuration Odoo trouvée."})

    try:
        # 2. Connexion au "bureau de sécurité" (common)
        common = xmlrpc.client.ServerProxy(f'{config.url}/xmlrpc/2/common')
        uid = common.authenticate(config.db, config.username, config.password, {})
        
        # 3. Connexion aux données (object)
        models = xmlrpc.client.ServerProxy(f'{config.url}/xmlrpc/2/object')

        # 4. Recherche des feedbacks filtrés par l'email de l'utilisateur connecté
        # Le filtre est : [['champ_odoo', '=', 'valeur_django']]
        domain = [[['application_id.email_from', '=', request.user.email]]]
        
        feedbacks = models.execute_kw(
            config.db, uid, config.password,
            'hr.feedback',  # Ton modèle Odoo
            'search_read',         # Action
            domain,                # Notre filtre sur l'email
            {'fields': ['display_name', 'average_score', 'description', 'create_date', 'author_id']} # Les champs à lire
        )

        # On envoie les résultats à la page HTML
        return render(request, 'feedback_portal/index.html', {'feedbacks': feedbacks})

    except Exception as e:
        # En cas d'erreur technique (Odoo éteint, mauvais mot de passe...)
        return render(request, 'feedback_portal/error.html', {'message': f"Erreur Odoo : {e}"})