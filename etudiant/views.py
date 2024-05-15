from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import AutorisationDeReclamation, Etudiant, Inscription, ResultatParMatiere, Semestre,Matiere, Reclamation
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout 
from .forms import ConnexionForm
from .models import Etudiant
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.contrib import auth


def saisie_matricule(request):
    if request.method == 'POST':
        matricule = request.POST['matricule']
        semestre_id_selectionne = request.POST.get('semestre', None)
        try:
            etudiant = Etudiant.objects.get(matricule=matricule)
            inscription = Inscription.objects.get(etudiant=etudiant)
            
            if semestre_id_selectionne:
                # Récupérer le nom du semestre sélectionné
                semestre_selectionne = Semestre.objects.get(id_semestre=semestre_id_selectionne).Semestre
                # Logique pour filtrer les résultats en fonction du semestre sélectionné
                resultats = ResultatParMatiere.objects.filter(etudiant=etudiant, matiere__Semestre=semestre_id_selectionne)
                semestre_apres_selection = ResultatParMatiere.objects.filter(etudiant=etudiant)
                semestres = set(resultat.matiere.Semestre for resultat in semestre_apres_selection)
            else:
                # Récupérer tous les résultats de l'étudiant
                resultats = ResultatParMatiere.objects.filter(etudiant=etudiant)
                semestres = set(resultat.matiere.Semestre for resultat in resultats)
                semestre_selectionne = None

            autorisations_ouvertes = AutorisationDeReclamation.objects.filter(Etat='OU')
             # Vérifier s'il y a des autorisations ouvertes
            autorisation_existante = True if autorisations_ouvertes else False
            context = {
                'nom': etudiant.user.first_name,
                'prenom': etudiant.user.last_name,
                'niveau': inscription.niveau.niveau,
                'matricule': matricule,
                'filiere' : etudiant.filiere.nom,
                'resultats': resultats,
                'semestres': semestres,
                'semestre_selectionne' : semestre_selectionne,
                'annee_univ' : inscription.annee_univ.annee_univ,
                'autorisations_ouvertes': autorisations_ouvertes, 
                'autorisation_existante': autorisation_existante
            }
            return render(request, 'infos_etudiant.html', context)
        except Etudiant.DoesNotExist:
            return render(request, 'etudiant_non_trouve.html')
    else:
        return render(request, 'saisie_matricule.html')

def auth_etudiant(request):
    error_message = None

    if request.method == 'POST':
        email = request.POST.get('email')
        mot_de_passes = request.POST.get('mot_de_passe')

        user = authenticate(request, username=email, password=mot_de_passes)
        if user is not None:
            login(request, user)
            # Récupérer l'URL à laquelle l'utilisateur tentait d'accéder avant la connexion
            redirect_to = request.GET.get('next', 'profil_etudiant')
            # Rediriger l'utilisateur vers cette URL ou vers la page de profil étudiant par défaut
            return redirect(redirect_to)
        else:
            error_message = "Adresse e-mail ou mot de passe incorrect."

    return render(request, 'AuthEtudiant.html', {'error_message': error_message})



@login_required
def create_reclamation(request):
    autorisations_ouvertes = AutorisationDeReclamation.objects.filter(Etat='OU')

    if not autorisations_ouvertes.exists():
        # Si une autorisation de réclamation est ouverte, rediriger l'utilisateur
        return redirect('saisie_matricule') 
   # Récupérer l'étudiant authentifié
    etudiant = request.user.etudiant

    # Récupérer le dernier semestre du niveau de l'étudiant
    dernier_semestre = Semestre.objects.filter(niveau_obj=etudiant.inscription_set.first().niveau).latest('id_semestre')

    if request.method == 'POST':
        # Récupérer les données du formulaire
        contenu = request.POST.get('contenu')
        preuve_reclamation = request.FILES.get('preuve_reclamation')
        matiere_id = request.POST.get('Matiere')

        # Créer la réclamation
        reclamation = Reclamation.objects.create(
            contenu=contenu,
            preuve_reclamation=preuve_reclamation,
            etudiant=etudiant,
            date_reclamation=now(),
            status="en attente",
            Matiere_id=matiere_id
        )
        # Associer la matière à la réclamation
        if matiere_id:
            matiere = Matiere.objects.get(code=matiere_id)
            reclamation.Matiere = matiere
            reclamation.save()

        return redirect('reclamation_success')  # Rediriger vers une page de succès

    # Récupérer les matières du dernier semestre du niveau de l'étudiant
    matieres_semestre = Matiere.objects.filter(Semestre=dernier_semestre, filiere=etudiant.filiere)

    # Si la méthode de la requête n'est pas POST, rendre le template avec un formulaire vide
    return render(request, 'reclamation_form.html', {'matieres': matieres_semestre})
@login_required
def reclamation_success(request):
    return render(request, 'reclamation_success.html')


# ### Profile

@login_required
def profil_etudiant(request):
    # Récupérer l'utilisateur connecté
    user = request.user

    # Récupérer le profil de l'étudiant s'il existe
    try:
        etudiant = Etudiant.objects.get(user=user)
    except Etudiant.DoesNotExist:
        etudiant = None

    # Récupérer les réclamations de l'étudiant s'il existe
    if etudiant:
        reclamations = Reclamation.objects.filter(etudiant=etudiant)
    else:
        reclamations = None

    context = {
        'etudiant': etudiant,
        'reclamations': reclamations
    }

    return render(request, 'profil_etudiant.html', context)

def logout_etudiant(request):
    if request.method == 'POST':
        auth.logout(request)
    return redirect('saisie_matricule')