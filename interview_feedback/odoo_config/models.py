from django.db import models
import xmlrpc.client

class OdooConfig(models.Model):
    url = models.URLField(
        verbose_name="URL de l'instance Odoo",
        default = "http://localhost:8069"
    )

    db = models.CharField(
        max_length = 100,
        verbose_name = "Nom de la base de données Odoo"
    )

    username = models.CharField(
        max_length = 100,
        verbose_name="Email de l'utilisateur Odoo"
    )

    password = models.CharField(
        max_length = 100,
        verbose_name="Mot de passe de l'utilisateur Odoo"
    )

    def __str__(self):
        return f"Configuration Odoo ({self.url}, {self.db}, {self.username})"
    
    def test_connection(self):
        try:
            # self.url : localhost de la config
            # /xmlrpc/2/common : C'est l'extension directe pour le service "Authentification" d'Odoo.
            # f au début : C'est une fonction Python (f-string) qui sert juste à coller les deux morceaux ensemble proprement.
            common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
            
            # 2. On demande à Odoo de nous authentifier (uid)
            # La méthode 'authenticate' prend : db, username, password, et une liste vide
            uid = common.authenticate(self.db, self.username, self.password, {})
            
            if uid: # ton numéro unique dans la base de données.
                return f"Succès ! Connexion réussie (UID: {uid})"
            else:
                return "Échec : Identifiants incorrects."
                
        except Exception as e:
            return f"Erreur de connexion : {e}"