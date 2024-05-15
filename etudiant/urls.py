from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.saisie_matricule, name='saisie_matricule'),
    # path('Reclamer/', views.Reclamer, name='Reclamer'),
    path('login/', views.auth_etudiant, name='login'),
    # path('fait/', views.faitreclamer, name='reclamer'),  
    path('reclamation/create/', views.create_reclamation, name='create_reclamation'),
    path('reclamation/success/', views.reclamation_success, name='reclamation_success'),
    path('logout/', views.logout_etudiant, name="logout_etudiant"),
        
    path('profil/', views.profil_etudiant, name='profil_etudiant'),

]
