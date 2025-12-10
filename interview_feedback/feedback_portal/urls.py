from django.urls import path
from . import views

urlpatterns = [
    # 1. La racine du site ('') affiche le formulaire de connexion
    path('', views.login_candidate, name='login_candidate'),

    # 2. Cette URL affiche les résultats (l'index)
    path('feedbacks/', views.index, name='index'),

    # 3. L'action de déconnexion
    path('logout/', views.logout_candidate, name='logout'),
]