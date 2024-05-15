from django import forms
from .models import Etudiant
from django import forms
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
class ConnexionForm(forms.Form):
    email = forms.EmailField(max_length=40)
    mot_de_passe = forms.CharField(max_length=40, widget=forms.PasswordInput)

    def clean_mot_de_passe(self):
        mot_de_passe = self.cleaned_data.get('mot_de_passe')
        # Ajouter ici votre validation personnalisée
        if len(mot_de_passe) < 8:
            raise forms.ValidationError("Le mot de passe doit contenir au moins 8 caractères.")
        return mot_de_passe

