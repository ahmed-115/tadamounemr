from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from django.utils import timezone
from .models import Orphelin, Sponsor, Parrainage, TransactionFinanciere, Intermediaire
from .forms import OrphelinForm, SponsorForm, ParrainageForm, TransactionFinanciereForm, IntermediaireForm
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from datetime import date


# ================================
# ORPHELINS
# ================================

def orphelin_list(request):
    orphelins = Orphelin.objects.all().order_by('-date_creation')
    return render(request, 'orphelins/list.html', {'orphelins': orphelins})

def orphelin_add(request):
    if request.method == 'POST':
        form = OrphelinForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('orphelin_list')
    else:
        form = OrphelinForm()
    return render(request, 'orphelins/form.html', {'form': form})

def orphelin_edit(request, pk):
    orphelin = get_object_or_404(Orphelin, pk=pk)
    if request.method == 'POST':
        form = OrphelinForm(request.POST, request.FILES, instance=orphelin)
        if form.is_valid():
            form.save()
            return redirect('orphelin_list')
    else:
        form = OrphelinForm(instance=orphelin)
    return render(request, 'orphelins/form.html', {'form': form, 'object': orphelin})

def orphelin_delete(request, pk):
    orphelin = get_object_or_404(Orphelin, pk=pk)
    if request.method == 'POST':
        orphelin.delete()
        return redirect('orphelin_list')
    return render(request, 'orphelins/confirm_delete.html', {'object': orphelin})

def orphelin_detail(request, pk):
    orphelin = get_object_or_404(Orphelin, pk=pk)
    return render(request, 'orphelins/detail.html', {'orphelin': orphelin})

def orphelin_search(request):
    query = Q()
    code = request.GET.get('code')
    nom = request.GET.get('nom')
    telephone = request.GET.get('telephone')

    if code:
        query &= Q(code__icontains=code)
    if nom:
        query &= Q(nom_complet__icontains=nom)
    if telephone:
        query &= Q(telephone_tuteur__icontains=telephone)

    orphelins = Orphelin.objects.filter(query).order_by('-date_creation')
    return render(request, 'orphelins/search_list.html', {'orphelins': orphelins})

def orphelin_statistiques(request):
    total = Orphelin.objects.count()
    sexe_count = Orphelin.objects.values('genre').annotate(count=Count('id'))
    scolarite_count = Orphelin.objects.values('scolarite').annotate(count=Count('id'))

    # Regrouper par âge
    now = timezone.now().date()
    age_groups = {
        'moins_6': Orphelin.objects.filter(date_naissance__gt=now.replace(year=now.year-6)).count(),
        '6_12': Orphelin.objects.filter(date_naissance__lte=now.replace(year=now.year-6),
                                        date_naissance__gt=now.replace(year=now.year-12)).count(),
        '12_18': Orphelin.objects.filter(date_naissance__lte=now.replace(year=now.year-12),
                                         date_naissance__gt=now.replace(year=now.year-18)).count(),
        '18_plus': Orphelin.objects.filter(date_naissance__lte=now.replace(year=now.year-18)).count(),
    }

    context = {
        'total': total,
        'sexe_count': sexe_count,
        'scolarite_count': scolarite_count,
        'age_groups': age_groups
    }
    return render(request, 'orphelins/statistiques.html', context)

def liste_parrainage(request, type_kafala):
    parrainages = Parrainage.objects.filter(type_kafala=type_kafala)
    orphelins = [p.orphelin for p in parrainages]
    return render(request, 'orphelins/liste_parrainage.html', {'orphelins': orphelins, 'type_kafala': type_kafala})



def parrainage_list(request):
    q = request.GET.get('q', '').strip()
    type_kafala = request.GET.get('type_kafala', '')
    statut = request.GET.get('statut', '')

    parrainages = Parrainage.objects.select_related(
        'orphelin', 'sponsor', 'intermediaire'
    )

    # 🔍 Recherche
    if q:
        parrainages = parrainages.filter(
            Q(orphelin__code__icontains=q) |
            Q(orphelin__nom_complet__icontains=q) |
            Q(sponsor__nom__icontains=q)
        )

    # 🎯 Filtres
    if type_kafala:
        parrainages = parrainages.filter(type_kafala=type_kafala)

    if statut:
        parrainages = parrainages.filter(statut=statut)

    return render(
        request,
        'parrainages/list.html',
        {
            'parrainages': parrainages,
            'q': q,
            'type_kafala': type_kafala,
            'statut': statut,
        }
    )



def feuille_mensuelle(request, type_kafala):
    now = timezone.now()
    mois = now.month
    annee = now.year
    parrainages = Parrainage.objects.filter(type_kafala=type_kafala, date_debut__month=mois, date_debut__year=annee)
    return render(request, 'orphelins/feuille_mensuelle.html', {'parrainages': parrainages, 'mois': mois, 'annee': annee, 'type_kafala': type_kafala})

def suivi_orphelin(request, pk):
    orphelin = get_object_or_404(Orphelin, pk=pk)
    parrainages = Parrainage.objects.filter(orphelin=orphelin)
    transactions = TransactionFinanciere.objects.filter(parrainage__in=parrainages)
    return render(request, 'orphelins/suivi.html', {'orphelin': orphelin, 'parrainages': parrainages, 'transactions': transactions})

# ================================
# SPONSORS
# ================================

def sponsor_list(request):
    sponsors = Sponsor.objects.all()
    return render(request, 'sponsors/list.html', {'sponsors': sponsors})

def sponsor_add(request):
    if request.method == 'POST':
        form = SponsorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sponsor_list')
    else:
        form = SponsorForm()
    return render(request, 'sponsors/form.html', {'form': form})

def sponsor_edit(request, pk):
    sponsor = get_object_or_404(Sponsor, pk=pk)
    if request.method == 'POST':
        form = SponsorForm(request.POST, instance=sponsor)
        if form.is_valid():
            form.save()
            return redirect('sponsor_list')
    else:
        form = SponsorForm(instance=sponsor)
    return render(request, 'sponsors/form.html', {'form': form, 'object': sponsor})

# ================================
# PARRAINAGES
# ================================

# def parrainage_list(request):
#     parrainages = Parrainage.objects.all()
#     return render(request, 'parrainages/list.html', {'parrainages': parrainages})

def parrainage_add(request):
    if request.method == 'POST':
        form = ParrainageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('parrainage_list')
    else:
        form = ParrainageForm()
    return render(request, 'parrainages/form.html', {'form': form})

def parrainage_edit(request, pk):
    parrainage = get_object_or_404(Parrainage, pk=pk)
    if request.method == 'POST':
        form = ParrainageForm(request.POST, instance=parrainage)
        if form.is_valid():
            form.save()
            return redirect('parrainage_list')
    else:
        form = ParrainageForm(instance=parrainage)
    return render(request, 'parrainages/form.html', {'form': form, 'object': parrainage})


def parrainage_detail(request, pk):
    parrainage = get_object_or_404(
        Parrainage.objects.select_related(
            'orphelin',
            'sponsor',
            'intermediaire'
        ),
        pk=pk
    )

    return render(request, 'parrainages/detail.html', {
        'p': parrainage
    })

# ================================
# TRANSACTIONS FINANCIERES
# ================================

# def transaction_list(request):
#     transactions = TransactionFinanciere.objects.all()
#     return render(request, 'transactions/list.html', {'transactions': transactions})


def transaction_list(request):
    today = date.today()

    # valeurs par défaut
    mois = request.GET.get('mois') or today.month
    annee = request.GET.get('annee') or today.year
    sponsor_id = request.GET.get('sponsor')

    transactions = TransactionFinanciere.objects.select_related(
        'parrainage__orphelin',
        'parrainage__sponsor'
    ).filter(
        date_creation__month=mois,
        date_creation__year=annee
    )

    # filtre par الكافل (Sponsor)
    if sponsor_id:
        transactions = transactions.filter(
            parrainage__sponsor_id=sponsor_id
        )

    sponsors = Sponsor.objects.all()

    context = {
        'transactions': transactions,
        'mois': int(mois),
        'annee': int(annee),
        'sponsors': sponsors,
        'sponsor_id': sponsor_id,
    }
    return render(request, 'transactions/list.html', context)



def transaction_add(request):
    if request.method == 'POST':
        form = TransactionFinanciereForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.cree_par = request.user
            transaction.type_transaction = 'sortie'
            transaction.save()

            # Mettre à jour le solde
            if transaction.parrainage:
                parrainage = transaction.parrainage
                parrainage.solde -= transaction.montant
                parrainage.save()

            return redirect('transaction_list')
    else:
        form = TransactionFinanciereForm()
    return render(request, 'transactions/form.html', {'form': form})


# def transaction_add(request):
#     if request.method == 'POST':
#         form = TransactionFinanciereForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('transaction_list')
#     else:
#         form = TransactionFinanciereForm()
#     return render(request, 'transactions/form.html', {'form': form})

def transaction_edit(request, pk):
    transaction = get_object_or_404(TransactionFinanciere, pk=pk)
    if request.method == 'POST':
        form = TransactionFinanciereForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TransactionFinanciereForm(instance=transaction)
    return render(request, 'transactions/form.html', {'form': form, 'object': transaction})


# ================================
# TRANSACTIONS Intermediaire
# ================================

# Liste
def intermediaire_list(request):
    intermediaires = Intermediaire.objects.all()
    return render(request, 'intermediaires/list.html', {'intermediaires': intermediaires})

# Ajouter
def intermediaire_add(request):
    if request.method == 'POST':
        form = IntermediaireForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('intermediaire_list')
    else:
        form = IntermediaireForm()
    return render(request, 'intermediaires/form.html', {'form': form})

# Modifier
def intermediaire_edit(request, pk):
    intermediaire = get_object_or_404(Intermediaire, pk=pk)
    if request.method == 'POST':
        form = IntermediaireForm(request.POST, instance=intermediaire)
        if form.is_valid():
            form.save()
            return redirect('intermediaire_list')
    else:
        form = IntermediaireForm(instance=intermediaire)
    return render(request, 'intermediaires/form.html', {'form': form, 'object': intermediaire})



@login_required
def dashboard(request):
    return render(request, 'dashboard.html')
