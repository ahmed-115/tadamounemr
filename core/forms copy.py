# core/forms.py
from django import forms
from .models import Orphelin, Sponsor, Parrainage, TransactionFinanciere, Intermediaire

# ------------------------------
# Formulaire Orphelin
# ------------------------------
class OrphelinForm(forms.ModelForm):
    class Meta:
        model = Orphelin
        fields = [
            'nom_complet', 'nni', 'genre', 'date_naissance', 'nom_tuteur',
            'telephone_tuteur', 'adresse', 'latitude', 'longitude',
            'scolarite', 'niveau_scolaire', 'etat_sante', 'photo', 'dossier_pdf', 'statut'
        ]
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
        }

# ------------------------------
# Formulaire Sponsor
# ------------------------------
class SponsorForm(forms.ModelForm):
    class Meta:
        model = Sponsor
        fields = ['nom', 'type_sponsor', 'nationalite', 'telephone', 'email', 'adresse']

# ------------------------------
# Formulaire Parrainage
# ------------------------------
class ParrainageForm(forms.ModelForm):
    class Meta:
        model = Parrainage
        fields = [
            'orphelin', 'sponsor', 'intermediaire', 'type_kafala',
            'montant_mru', 'montant_devise', 'devise', 'solde',
            'date_debut', 'date_fin', 'statut'
        ]
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
        }

# ------------------------------
# Formulaire Transaction Financière
# ------------------------------
class TransactionFinanciereForm(forms.ModelForm):
    class Meta:
        model = TransactionFinanciere
        # On exclut les champs qu'on ne veut pas afficher
        exclude = ['type_transaction', 'cree_par', 'date_creation']


# ------------------------------
# Formulaire Intermediaire
# ------------------------------

class IntermediaireForm(forms.ModelForm):
    class Meta:
        model = Intermediaire
        fields = '__all__'