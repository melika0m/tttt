import os
import django
from django.contrib.auth.hashers import make_password

# Configuration de l'environnement Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "siteISCAE.settings")
django.setup()
from django.contrib.auth.models import User
from etudiant.models import Etudiant

# Définition des données pour les nouveaux étudiants
etudiants_data = [
    {
        "matricule": "I18001",
        "nni": 1234567890,
        "sexe": "H",
        "numero_telephone": 12345678,
        "filiere_id": "id_FC",
    },
    {
        "matricule": "I18002",
        "nni": 9876543210,
        "sexe": "H",
        "numero_telephone": 87654321,
        "filiere_id": "id_FC",
    },
    {
        "matricule": "I18003",
        "nni": 9876543210,
        "sexe": "H",
        "numero_telephone": 87654321,
        "filiere_id": "id_FC",
    },
    {
        "matricule": "I18004",
        "nni": 9876543210,
        "sexe": "H",
        "numero_telephone": 87654321,
        "filiere_id": "id_FC",
    },
    {
        "matricule": "I18005",
        "nni": 9876543210,
        "sexe": "H",
        "numero_telephone": 87654321,
        "filiere_id": "id_FC",
    },
    {
        "matricule": "I18006",
        "nni": 9876543210,
        "sexe": "H",
        "numero_telephone": 87654321,
        "filiere_id": "id_FC",
    },
    {
        "matricule": "I18007",
        "nni": 9876543210,
        "sexe": "H",
        "numero_telephone": 87654321,
        "filiere_id": "id_FC",
    },

    {
        "matricule": "I18008",
        "nni": 9876543210,
        "sexe": "H",
        "numero_telephone": 87654321,
        "filiere_id": "id_FC",
    },
    
    {
        "matricule": "I18009",
        "nni": 9876543210,
        "sexe": "F",
        "numero_telephone": 87654321,
        "filiere_id": "id_FC",
    },
    
    {
        "matricule": "I18010",
        "nni": 9876543210,
        "sexe": "F",
        "numero_telephone": 87654321,
        "filiere_id": "id_FC",
    },
    
    {
        "matricule": "I18011",
        "nni": 9876543210,
        "sexe": "F",
        "numero_telephone": 87654321,
        "filiere_id": "id_FC",
    },
    
    {
        "matricule": "I18012",
        "nni": 9876543210,
        "sexe": "F",
        "numero_telephone": 87654321,
        "filiere_id": "id_FC",
    },
    
    {
        "matricule": "I18013",
        "nni": 9876543210,
        "sexe": "F",
        "numero_telephone": 87654321,
        "filiere_id": "id_FC",
    },
    
    {
        "matricule": "I18014",
        "nni": 9876543210,
        "sexe": "F",
        "numero_telephone": 87654321,
        "filiere_id": "id_FC",
    },
    
    {
        "matricule": "I18015",
        "nni": 9876543210,
        "sexe": "H",
        "numero_telephone": 87654321,
        "filiere_id": "id_FC",
    },
    
    {
        "matricule": "I18016",
        "nni": 9876543210,
        "sexe": "F",
        "numero_telephone": 87654321,
        "filiere_id": "id_FC",
    },
    
    {
        "matricule": "I18017",
        "nni": 9876543210,
        "sexe": "F",
        "numero_telephone": 87654321,
        "filiere_id": "id_FC",
    },
    
    {
        "matricule": "I18018",
        "nni": 9876543210,
        "sexe": "F",
        "numero_telephone": 87654321,
        "filiere_id": "id_FC",
    },
    
    
    
    # Ajoutez d'autres étudiants ici
]

# Parcourir les données des nouveaux étudiants et les insérer dans la base de données
for etudiant_data in etudiants_data:
    # Créer un username se terminant par "@gmail.com"
    username = etudiant_data["matricule"] + "@gmail.com"

    # Créer un utilisateur Django avec mot de passe crypté
    new_user = User.objects.create(
        username=username,
        email=username,  # Utiliser le même email pour username
        password=make_password("motdepasse"),  # Utiliser le mot de passe crypté
    )

    # Créer un étudiant associé à l'utilisateur avec matricule commençant par I18004
    etudiant = Etudiant.objects.create(
        user=new_user,
        matricule=etudiant_data["matricule"],
        nni=etudiant_data["nni"],
        sexe=etudiant_data["sexe"],
        numero_telephone=etudiant_data["numero_telephone"],
        filiere_id=etudiant_data["filiere_id"],
    )
