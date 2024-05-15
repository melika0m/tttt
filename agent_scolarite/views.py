from datetime import timezone
from django.shortcuts import render
from etudiant.models import AgentDeScolarite,Reclamation
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse, Http404
from etudiant.models import AutorisationDeReclamation
from django import forms
from django.contrib.auth.models import User
from etudiant.models import Reclamation, Matiere,Semestre

def connexion(request):
    error_message = None

    if request.method == 'POST':
        email = request.POST.get('email')
        mot_de_passes = request.POST.get('mot_de_passe')

        user = authenticate(request, username=email, password=mot_de_passes)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            error_message = "Adresse e-mail ou mot de passe incorrect."

    return render(request, 'agent_scolarite/connexion.html', {'error_message': error_message})

from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.decorators import login_required


@login_required
def dashbord(request):
    try:
        # Vérifier si l'utilisateur a un objet AgentDeScolarite associé
        agent_de_scolarite = request.user.agentdescolarite
    except AgentDeScolarite.DoesNotExist:
        raise Http404("L'agent de scolarité associé à cet utilisateur n'existe pas.")

    total_reclamations = Reclamation.objects.all().count()
    total_reclamations_acceptees = Reclamation.objects.filter(status='Acceptee').count()
    total_reclamations_refusees = Reclamation.objects.filter(status='Refusée').count()
    total_reclamations_en_attente = Reclamation.objects.filter(status='En attente').count()
    total_reclamations_traitees = total_reclamations_acceptees + total_reclamations_refusees

    return render(request, 'agent_scolarite/dashbord.html', {
        'total_reclamations': total_reclamations,
        'total_reclamations_acceptees': total_reclamations_acceptees,
        'total_reclamations_refusees': total_reclamations_refusees,
        'total_reclamations_en_attente': total_reclamations_en_attente,
        'total_reclamations_traitees': total_reclamations_traitees,})


    
def logout_agent(request):
    if request.method == 'POST':
        auth.logout(request)
    return redirect('authentification')

@login_required
def periode_reclamation(request):
    try:
        # Vérifier si l'utilisateur a un objet AgentDeScolarite associé
        agent_de_scolarite = request.user.agentdescolarite
    except AgentDeScolarite.DoesNotExist:
        raise Http404("L'agent de scolarité associé à cet utilisateur n'existe pas.")

    if request.method == 'POST':
        date_expiration = request.POST.get('date_expiration')
        Etat = request.POST.get('Etat')

        # Créer une nouvelle autorisation de réclamation
        autorisation = AutorisationDeReclamation(
            date_expiration=date_expiration,
            Etat=Etat,
            AgentDeScolarite=agent_de_scolarite
        )

        # Si l'état est 'EX', définir la date d'expiration sur la date actuelle
        if Etat == 'EX':
            autorisation.date_expiration = timezone.now()

        autorisation.save()
        return redirect('periode_reclamation')
    else:
        # Récupérer les autorisations ouvertes pour l'agent de scolarité actuel
        autorisations_ouvertes = AutorisationDeReclamation.objects.filter(
            AgentDeScolarite=agent_de_scolarite,
            Etat='OU'
        )
        autorisations_ouvertes = AutorisationDeReclamation.objects.filter(Etat='OU')
    
    # Vérifier s'il y a des autorisations ouvertes
        autorisation_existante = True if autorisations_ouvertes else False
        context = {'user': request.user, 
                   'autorisations_ouvertes': autorisations_ouvertes, 
                   'autorisation_existante': autorisation_existante}
        return render(request, 'agent_scolarite/periodedeRclamation.html', context)
@login_required
def index(request):
    try:
        # Vérifier si l'utilisateur a un objet AgentDeScolarite associé
        agent_de_scolarite = request.user.agentdescolarite
    except AgentDeScolarite.DoesNotExist:
        raise Http404("L'agent de scolarité associé à cet utilisateur n'existe pas.")

    # Votre code pour le tableau de bord
    return render(request, 'agent_scolarite/index.html')

@login_required
def changer_etat_autorisation(request, autorisation_id, nouvel_etat):
    try:
        # Vérifier si l'utilisateur a un objet AgentDeScolarite associé
        agent_de_scolarite = request.user.agentdescolarite
    except AgentDeScolarite.DoesNotExist:
        raise Http404("L'agent de scolarité associé à cet utilisateur n'existe pas.")

    autorisation = get_object_or_404(AutorisationDeReclamation, id_autorisation=autorisation_id)
    autorisation.Etat = nouvel_etat
    autorisation.save()
    return redirect('periode_reclamation')

@login_required
def liste_des_reclamations(request):

    try:
        agent_de_scolarite = request.user.agentdescolarite
    except AgentDeScolarite.DoesNotExist:
        raise Http404("L'agent de scolarité associé à cet utilisateur n'existe pas.")

    reclamations = Reclamation.objects.all()
    return render(request, 'agent_scolarite/liste_des_reclamations.html', {'reclamations': reclamations})
@login_required
def accepter_reclamation(request, reclamation_id):
    try:
        agent_de_scolarite = request.user.agentdescolarite
    except AgentDeScolarite.DoesNotExist:
        raise Http404("L'agent de scolarité associé à cet utilisateur n'existe pas.")
    reclamation = Reclamation.objects.get(id_reclamation=reclamation_id)
    # Logique pour accepter la réclamation ici

    reclamation.status = "Acceptee"
    reclamation.save()

    return redirect('liste_des_reclamations')
@login_required
def refuser_reclamation(request, reclamation_id):
    try:
        agent_de_scolarite = request.user.agentdescolarite
    except AgentDeScolarite.DoesNotExist:
        raise Http404("L'agent de scolarité associé à cet utilisateur n'existe pas.")
    # Récupérer la réclamation correspondante ou retourner une erreur 404 si elle n'existe pas
    reclamation = get_object_or_404(Reclamation, id_reclamation=reclamation_id)

    # Mettre à jour le statut de la réclamation à "Refusée" (ou à toute autre valeur appropriée)
    reclamation.status = "Refusée"
    reclamation.save()

    # Rediriger vers la page de liste des réclamations après avoir refusé la réclamation
    return redirect('liste_des_reclamations')
@login_required
def changePassword(request):
    try:
        # Vérifier si l'utilisateur a un objet AgentDeScolarite associé
        agent_de_scolarite = request.user.agentdescolarite
    except AgentDeScolarite.DoesNotExist:
        raise Http404("L'agent de scolarité associé à cet utilisateur n'existe pas.")

    error = ""
    if not request.user.is_authenticated:
        return redirect('connexionAgent')  # Redirection vers la page de connexion si l'utilisateur n'est pas authentifié

    if request.method == "POST":
        old_password = request.POST.get('oldpassword')
        new_password = request.POST.get('newpassword')
        confirm_password = request.POST.get('confirmpassword')
        
        if new_password != confirm_password:
            error = 'Les mots de passe ne correspondent pas.'
        else:
            user = request.user
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                return render(request, 'agent_scolarite/change_password_success.html')
            else:
                error = 'Le mot de passe actuel est incorrect.'

    return render(request, 'agent_scolarite/change_password.html', {'error':error})


@login_required
def liste_des_reclamations(request):
    try:
        agent_de_scolarite = request.user.agentdescolarite
    except AgentDeScolarite.DoesNotExist:
        raise Http404("L'agent de scolarité associé à cet utilisateur n'existe pas.")

    semestres = Semestre.objects.all()  # Récupérer tous les semestres pour afficher dans le menu déroulant

    if request.method == 'GET' and 'Semestre_id' in request.GET:
        semestre_id = request.GET['Semestre_id']
        if semestre_id:
            matieres = Matiere.objects.filter(Semestre_id=semestre_id)  # Utilisation de la relation entre Matiere et Semestre
            reclamations = Reclamation.objects.filter(Matiere__in=matieres)
        else:
            reclamations = Reclamation.objects.all()
    else:
        reclamations = Reclamation.objects.all()

    return render(request, 'agent_scolarite/liste_des_reclamations.html', {'reclamations': reclamations, 'semestres': semestres})


def statistique(request):
    return render(request, 'agent_scolarite/statistique.html')

def dashbord(request):
    return render(request,'agent_scolarite/dashbord.html')

def listReclamation(request):
    return render(request,'agent_scolarite/listReclamation.html')

@login_required
def liste_reclamations_etudiant(request):
    return render(request, 'agent_scolarite/reclamations_etudiant.html')


@login_required
def reclamations_refusees(request):
    reclamations_refusees = Reclamation.objects.filter(status="Refusée")
    return render(request, 'agent_scolarite/reclamations_refusees.html', {'reclamations_refusees': reclamations_refusees})


@login_required
def reclamations_acceptees(request):
    reclamations_acceptees = Reclamation.objects.filter(status="acceptee")
    return render(request, 'agent_scolarite/reclamations_acceptees.html', {'reclamations_acceptees': reclamations_acceptees})


@login_required
def reclamations_par_matiere(request):
    reclamations_par_matiere = {}

    reclamations_acceptees = Reclamation.objects.filter(status="acceptee")

    for reclamation in reclamations_acceptees:
        matiere = reclamation.Matiere
        if matiere not in reclamations_par_matiere:
            reclamations_par_matiere[matiere] = []
        reclamations_par_matiere[matiere].append(reclamation)

    return render(request, 'agent_scolarite/reclamations_par_matiere.html', {'reclamations_par_matiere': reclamations_par_matiere})