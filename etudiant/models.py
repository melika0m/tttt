from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.utils import timezone

# Create your models here.

class Departement(models.Model):
    id_departement = models.CharField(max_length= 25,primary_key=True)
    nom_departement = models.CharField(max_length=40)
    responsable_departement = models.CharField(max_length=40)

class Filiere(models.Model):
    idF = models.CharField(max_length= 25,primary_key=True)
    nom = models.CharField(max_length=40)
    date_creation = models.DateField()
    domain = models.CharField(max_length=40)
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE)

class Etudiant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matricule = models.CharField(max_length=25, primary_key=True)
    nom = models.CharField(max_length=100, null= True)
    prenom = models.CharField(max_length=100, null= True)
    nni = models.BigIntegerField(default=0, blank=True)
    sexe = models.CharField(max_length=4)
    numero_telephone = models.BigIntegerField(default=0)
    filiere = models.ForeignKey('Filiere', on_delete=models.CASCADE, default='')


class AgentDeScolarite(models.Model):
    id_agent_scolarite = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100, null= True)
    prenom = models.CharField(max_length=100, null= True)
    numero_telephone = models.IntegerField()
    poste_agent_scolarite = models.CharField(max_length=255)

class AutorisationDeReclamation(models.Model):
    OUVERT = 'OU'
    FERME = 'FE'
    EXPIRE = 'EX'
    ETAT_CHOICES = [
        (OUVERT, 'Ouvert'),
        (FERME, 'Fermé'),
        (EXPIRE, 'Expiré'),
    ]
    id_autorisation = models.AutoField(primary_key=True)
    date_expiration = models.DateTimeField(default=timezone.now)
    date_autorisation = models.DateTimeField(default=timezone.now)
    AgentDeScolarite = models.ForeignKey(AgentDeScolarite, on_delete=models.CASCADE)
    Etat = models.CharField(max_length=2, choices=ETAT_CHOICES, default=OUVERT)

class Niveau(models.Model):
    id_niveau = models.CharField(max_length= 25,primary_key=True)
    niveau = models.CharField(max_length=20)

class Semestre(models.Model):
    id_semestre = models.CharField(max_length= 25,primary_key=True)
    Semestre = models.CharField(max_length=25)
    niveau_obj = models.ForeignKey(Niveau, on_delete=models.CASCADE)


class Matiere(models.Model):
    code = models.CharField(max_length= 25,primary_key=True)
    titre = models.CharField(max_length=30)
    credit = models.IntegerField()
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    Semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)
    

class Reclamation(models.Model):
    id_reclamation = models.AutoField(primary_key=True)
    contenu = models.TextField()
    preuve_reclamation = models.FileField(null= True, upload_to='documents/reclamations/', validators=[FileExtensionValidator(allowed_extensions=['pdf','png','jpg'])])
    status = models.CharField(max_length=30)
    type = models.CharField(max_length=30, null=True)
    date_reclamation = models.DateField()
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    Matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)

class Notification(models.Model):
    id_notification = models.AutoField(primary_key=True)
    contenu = models.TextField()
    date_notification = models.DateField()
    delai = models.IntegerField()
    reclamation = models.ForeignKey(Reclamation, on_delete=models.CASCADE)
    agent_scolarite = models.ForeignKey(AgentDeScolarite, on_delete=models.CASCADE)

class AnneeUniv(models.Model):
    id_annee_univ = models.CharField(max_length= 20,primary_key=True)
    annee_univ = models.CharField(max_length=20)

class Inscription(models.Model):
    id_inscription = models.AutoField(primary_key=True)
    date_inscription = models.DateTimeField()
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE)
    annee_univ = models.ForeignKey(AnneeUniv, on_delete=models.CASCADE)

class ResultatParMatiere(models.Model):
    id_res_element = models.AutoField(primary_key=True)
    note_cc = models.FloatField()
    note_ex = models.FloatField()
    note_finale = models.FloatField()
    note_rattrapage = models.FloatField()
    validation = models.CharField(max_length=40)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    annee_universitaire = models.ForeignKey(AnneeUniv, on_delete=models.CASCADE)

class ResultatParMoyenGeneral(models.Model):
    id_res_par_moy_g = models.AutoField(primary_key=True)
    id_annee_diplome = models.CharField(max_length=40)
    moy_g = models.FloatField()
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)
    annee_univ = models.ForeignKey(AnneeUniv, on_delete=models.CASCADE)