
import getpass # Pour masquer la saisie du mot de passe
import xmlrpc.client
import sys # Pour permettre l'arrêt propre du script en cas d'erreur

# --- Variables de Connexion (À adapter si nécessaire) ---
url = "http://localhost:8069"
db = "projectDb"  # Nom de la base de données Odoo

# On demande l'email à l'utilisateur
username = input("Email : ")   # 63731@etu.he2b.be

# On demande le mot de passe sans l'afficher
password = getpass.getpass("Password : ")   #admin


# --- 1. Connexion et Authentification ---
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))

# Le script a bien pu atteindre l'URL (http://localhost:8069).
print("Version du serveur Odoo : ", common.version())

try:
    # Authentification et récupération de l'UID
    uid = common.authenticate(db, username, password, {})
    # Échec d'Authentification (Identifiants Invalides)
    if not uid:
        print("\n--- ERREUR : Échec de l'authentification (UID non valide). ---")
        print("Vérifiez la DB, l'utilisateur et le mot de passe.")
        sys.exit(1)
# Échec de Connexion (Problème Serveur)
except Exception as e:
    print(f"\n--- ERREUR : Impossible de se connecter au serveur. ---")
    print(f"Détail: {e}")
    sys.exit(1)

print(f"Authentification réussie. User ID (UID): {uid}")

# Connexion au service XML-RPC pour les modèles
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# --- 2. Vérification des Droits ---
print("\n--- VÉRIFICATION DES DROITS ('read') ---")
hasRight = models.execute_kw(
    db, uid, password,
    'hr.feedback', 'check_access_rights',
    ['read'], {'raise_exception': False}
)

if not hasRight:
    print("--- ACCÈS REFUSÉ. L'utilisateur n'a pas les droits de lecture. ---")
    sys.exit(1)

print("Droits de lecture accordés.")


print("-" * 30)

# --- 3. Boucle de recherche ---
while True:
    print("\nEntrez une partie du nom de l'auteur pour chercher des feedbacks.")
    print("(Laissez vide et appuyez sur Entrée pour quitter)")
    
    author_name = input("Nom de l'auteur : ")

    # Condition de sortie de la boucle
    if not author_name:
        print("Fin du programme.")
        break

    print(f"Recherche des feedbacks pour l'auteur contenant : '{author_name}'...")

    # APPEL XML-RPC : search_read
 
    # execute_kw(base_de_données, identifiant_utilisateur, mot_de_passe,
    # nom_du_modèle, nom_de_la_méthode, arguments, options)

    feedbacks = models.execute_kw(
        db, uid, password,
        'hr.feedback', 'search_read',
        [[['author_id.name', 'ilike', author_name]]], # Le Domaine (Filtre)
        {'fields': ['author_id', 'description', 'state', 'application_id', 'average_score']} # Champs à lire
    )

    if feedbacks:  #verifier si liste vide
        print(f"--> {len(feedbacks)} feedback(s) trouvé(s) :\n")
        for f in feedbacks:
            # author_id est un tuple (id, "Nom"), on prend le 2ème élément pour l'affichage
            a_name = f['author_id'][1] if f['author_id'] else "Inconnu"
            
            print(f"ID: {f['id']} | Auteur: {a_name} | Score: {f['average_score']}/10")
            print(f"Description: {f['description']}")
            print("-" * 20)
    else:
        print("--> Aucun feedback trouvé.")


