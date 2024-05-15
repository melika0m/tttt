from django.urls import path
from . import views

urlpatterns = [
    # Autres URL de votre application
    # path('lister_agents/', views.lister_agents, name='lister_agents'),
    path('', views.connexion, name='authentification'),
    path('index/', views.index, name='index'),
    path('periode_reclamation/', views.periode_reclamation, name='periode_reclamation'),

    path('logout/', views.logout_agent, name="logout_agent"),
    path('change_password/', views.changePassword, name='change_password'),
    path('liste_des_reclamations/', views.liste_des_reclamations, name='liste_des_reclamations'),
    path('accepter_reclamation/<int:reclamation_id>/', views.accepter_reclamation, name='accepter_reclamation'),
    path('refuser_reclamation/<int:reclamation_id>/', views.refuser_reclamation, name='refuser_reclamation'), 
    path('changer_etat_autorisation/<int:autorisation_id>/<str:nouvel_etat>/', views.changer_etat_autorisation, name='changer_etat_autorisation'),
    # path('update_autorisation_state/', views.update_autorisation_state, name='update_autorisation_state'),
    path('reclamations_acceptees/', views.reclamations_acceptees, name='reclamations_acceptees'),
    path('reclamations_refusees/', views.reclamations_refusees, name='reclamations_refusees'), 
    path('reclamations_par_matiere/', views.reclamations_par_matiere, name='reclamations_par_matiere'),
    path('statistique/', views.statistique, name='statistique'),
    path('dashbord/', views.dashbord, name='dashbord'),
    path('listReclamation/', views.listReclamation, name='listReclamation'),
]