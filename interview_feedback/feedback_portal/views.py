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

# --- VUE 3 : INDEX (Liste des feedbacks avec Filtre) ---
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

        # --- GESTION DU FILTRE ---
        # On récupère le choix de l'utilisateur ('all' par défaut)
        filter_option = request.GET.get('filter', 'all')

        # On crée la liste des critères de recherche (le domaine Odoo)
        # Critère de base : l'email du candidat
        search_domain = [['application_id.email_from', '=', candidate_email]]

        # On ajoute les critères supplémentaires selon le filtre choisi
        if filter_option == 'high':
            # Note > 6 sur 10
            search_domain.append(['average_score', '>', 6])
        elif filter_option == 'low':
            # Note <= 6 sur 10
            search_domain.append(['average_score', '<=', 6])

        # 4. Appel XML-RPC
        # Note : execute_kw attend une liste d'arguments. Le premier argument est notre domaine.
        # Donc on met [search_domain]
        feedbacks = models.execute_kw(
            config.db, uid, config.password,
            'hr.feedback',
            'search_read',
            [search_domain], 
            {'fields': ['display_name', 'average_score', 'description', 'create_date', 'author_id']}
        )

        return render(request, 'feedback_portal/index.html', {
            'feedbacks': feedbacks,
            'user_email': candidate_email,
            'current_filter': filter_option # On renvoie le choix pour l'afficher dans le menu
        })

    except Exception as e:
        return render(request, 'feedback_portal/error.html', {'message': f"Erreur Odoo : {e}"})