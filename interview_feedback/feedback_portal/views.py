from django.shortcuts import render, redirect
import xmlrpc.client
from odoo_config.models import OdooConfig

# --- VUE 1 : LOGIN (Page d'accueil) ---
def login_candidate(request):
    # Si on envoie le formulaire (POST)
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            # On enregistre l'email en session
            request.session['candidate_email'] = email
            # On redirige vers la liste des feedbacks (nom de l'url : 'index')
            return redirect('index')
            
    # Sinon, on affiche juste le HTML du login
    return render(request, 'feedback_portal/login.html')

# --- VUE 2 : LOGOUT ---
def logout_candidate(request):
    try:
        del request.session['candidate_email']
    except KeyError:
        pass
    return redirect('login_candidate')

# --- VUE 3 : INDEX (Liste des feedbacks) ---
def index(request):
    # 1. Sécurité : On vérifie si l'email est en session
    candidate_email = request.session.get('candidate_email')
    if not candidate_email:
        return redirect('login_candidate')

    # 2. Config Odoo
    config = OdooConfig.objects.first()
    if not config:
        return render(request, 'feedback_portal/error.html', {'message': "Pas de configuration Odoo."})

    try:
        # 3. Connexion XML-RPC
        common = xmlrpc.client.ServerProxy(f'{config.url}/xmlrpc/2/common')
        uid = common.authenticate(config.db, config.username, config.password, {})
        
        models = xmlrpc.client.ServerProxy(f'{config.url}/xmlrpc/2/object')

        # 4. Recherche filtrée sur l'email en session
        domain = [[['application_id.email_from', '=', candidate_email]]]
        
        feedbacks = models.execute_kw(
            config.db, uid, config.password,
            'hr.feedback',
            'search_read',
            domain,
            {'fields': ['display_name', 'average_score', 'description', 'create_date', 'author_id']}
        )

        return render(request, 'feedback_portal/index.html', {
            'feedbacks': feedbacks,
            'user_email': candidate_email
        })

    except Exception as e:
        return render(request, 'feedback_portal/error.html', {'message': f"Erreur Odoo : {e}"})