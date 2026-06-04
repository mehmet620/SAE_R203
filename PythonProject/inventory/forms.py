from django import forms
from django.core.exceptions import ValidationError
from .models import TypeServeur, Serveur, Utilisateur, Service, Application, UsageRessource


class TypeServeurForm(forms.ModelForm):
    class Meta:
        model  = TypeServeur
        fields = ['type', 'description']


class ServeurForm(forms.ModelForm):
    class Meta:
        model  = Serveur
        fields = ['nom', 'type_serveur', 'nombre_processeur', 'capacite_memoire', 'capacite_stockage']


class UtilisateurForm(forms.ModelForm):
    class Meta:
        model  = Utilisateur
        fields = ['nom', 'prenom', 'email']


class ApplicationForm(forms.ModelForm):
    class Meta:
        model  = Application
        fields = ['nom_application', 'logo', 'utilisateur']


class ServiceForm(forms.ModelForm):
    class Meta:
        model   = Service
        fields  = ['nom_service', 'date_lancement', 'espace_memoire_utilise', 'memoire_vive_necessaire', 'serveur']
        widgets = {'date_lancement': forms.DateInput(attrs={'type': 'date'})}

    def clean(self):
        cleaned = super().clean()
        serveur = cleaned.get('serveur')
        utilise = cleaned.get('espace_memoire_utilise')
        ram     = cleaned.get('memoire_vive_necessaire')

        if serveur and utilise is not None and ram is not None:
            utilise_deja = sum(
                s.espace_memoire_utilise for s in serveur.services.all()
                if self.instance.pk is None or s.pk != self.instance.pk
            )
            libre = serveur.capacite_memoire - utilise_deja

            if utilise > libre:
                raise ValidationError(f"Mémoire insuffisante : {libre} Go libres, {utilise} Go demandés.")
            if ram > libre:
                raise ValidationError(f"RAM insuffisante : {libre} Go libres, {ram} Go requis.")

        return cleaned


class UsageRessourceForm(forms.ModelForm):
    class Meta:
        model  = UsageRessource
        fields = ['application', 'service']


class JSONImportForm(forms.Form):
    json_file = forms.FileField(label='Fichier JSON (.json)')

    def clean_json_file(self):
        f = self.cleaned_data['json_file']
        if not f.name.endswith('.json'):
            raise ValidationError("Le fichier doit avoir l'extension .json")
        return f
