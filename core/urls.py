from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # ================================
    # ORPHELINS
    # ================================
    path('orphelins/', views.orphelin_list, name='orphelin_list'),
    path('orphelins/ajouter/', views.orphelin_add, name='orphelin_add'),
    path('orphelins/<int:pk>/modifier/', views.orphelin_edit, name='orphelin_edit'),
    path('orphelins/<int:pk>/supprimer/', views.orphelin_delete, name='orphelin_delete'),
    path('orphelins/<int:pk>/detail/', views.orphelin_detail, name='orphelin_detail'),
    path('orphelins/<int:pk>/print/', views.orphelin_print, name='orphelin_print'),
    path('orphelins/recherche/', views.orphelin_search, name='orphelin_search'),
    path('orphelins/statistiques/', views.orphelin_statistiques, name='orphelin_statistiques'),
    # path('orphelins/liste_parrainage/<str:type_kafala>/', views.liste_parrainage, name='liste_parrainage'),
    # path('orphelins/feuille_mensuelle/<str:type_kafala>/', views.feuille_mensuelle, name='feuille_mensuelle'),
    path('orphelins/<int:pk>/suivi/', views.suivi_orphelin, name='suivi_orphelin'),
    path('orphelins/<int:pk>/suivi/print/', views.suivi_orphelin_print, name='suivi_orphelin_print'),

    # ================================
    # SPONSORS
    # ================================
    path('sponsors/', views.sponsor_list, name='sponsor_list'),
    path('sponsors/ajouter/', views.sponsor_add, name='sponsor_add'),
    path('sponsors/<int:pk>/modifier/', views.sponsor_edit, name='sponsor_edit'),

    # ================================
    # PARRAINAGES
    # ================================
    path('parrainages/', views.parrainage_list, name='parrainage_list'),
    path('parrainages/ajouter/', views.parrainage_add, name='parrainage_add'),
    path('parrainages/<int:pk>/modifier/', views.parrainage_edit, name='parrainage_edit'),
    path('parrainages/<int:pk>/detail/', views.parrainage_detail, name='parrainage_detail'),
    path('parrainages/<int:pk>/print/', views.kafala_print, name='kafala_print'),

    # ================================
    # TRANSACTIONS FINANCIERES
    # ================================
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/ajouter/', views.transaction_add, name='transaction_add'),
    path('transactions/<int:pk>/modifier/', views.transaction_edit, name='transaction_edit'),

    # ================================
    # TRANSACTIONS Intermediaire
    # ================================

    path('intermediaires/', views.intermediaire_list, name='intermediaire_list'),
    path('intermediaires/ajouter/', views.intermediaire_add, name='intermediaire_add'),
    path('intermediaires/<int:pk>/modifier/', views.intermediaire_edit, name='intermediaire_edit'),
    
    # ================================
    # AUTH
    # ================================
    path('', views.dashboard, name='dashboard'), 
    path('login/', auth_views.LoginView.as_view(template_name='login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),


    # ================================
    # PAIEMENT
    # ================================
    path('paiement/kafalat/', views.paiement_kafalat_form, name='paiement_kafalat_form'),
    path('paiement/kafalat/preview/', views.paiement_kafalat_preview, name='paiement_kafalat_preview'),
    path('paiement/kafalat/confirm/', views.paiement_kafalat_confirm, name='paiement_kafalat_confirm'),


]
