from django.contrib import admin
from django.utils.html import format_html

from .models import (
    User,
    Orphelin,
    Sponsor,
    Intermediaire,
    Parrainage,
    TransactionFinanciere,
    JournalAudit,
)

# =====================================================
# 👤 USERS
# =====================================================
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'role',
        'telephone',
        'is_active',
        'is_staff',
    )

    list_filter = (
        'role',
        'is_active',
        'is_staff',
    )

    search_fields = (
        'username',
        'email',
        'telephone',
    )


# =====================================================
# 👶 ORPHELINS
# =====================================================
@admin.register(Orphelin)
class OrphelinAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'nom_complet',
        'nni',
        'genre',
        'scolarite',
        'statut',
        'photo_preview',
    )

    list_filter = (
        'genre',
        'scolarite',
        'statut',
    )

    search_fields = (
        'code',
        'nom_complet',
        'nni',
        'nom_tuteur',
        'telephone_tuteur',
    )

    readonly_fields = (
        'code',
        'photo_preview',
        'dossier_preview',
        'date_creation',
    )

    fieldsets = (
        ('🧒 معلومات اليتيم', {
            'fields': (
                'code',
                'nom_complet',
                'nni',
                'genre',
                'date_naissance',
                'photo',
                'photo_preview',
                'dossier_pdf',
                'dossier_preview',
                'statut',
                'date_creation',
            )
        }),
        ('👨‍👩‍👦 الولي', {
            'fields': (
                'nom_tuteur',
                'telephone_tuteur',
            )
        }),
        ('🎓 التمدرس', {
            'fields': (
                'scolarite',
                'niveau_scolaire',
            )
        }),
        ('🏠 السكن', {
            'fields': (
                'adresse',
                'latitude',
                'longitude',
            )
        }),
        ('🏥 الحالة الصحية', {
            'fields': (
                'etat_sante',
            )
        }),
    )

    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" width="80" style="border-radius:10px;" />',
                obj.photo.url
            )
        return "—"
    photo_preview.short_description = "الصورة"

    def dossier_preview(self, obj):
        if obj.dossier_pdf:
            return format_html(
                '<a href="{}" target="_blank">📄 عرض الملف</a>',
                obj.dossier_pdf.url
            )
        return "—"
    dossier_preview.short_description = "ملف اليتيم"


# =====================================================
# 🤝 SPONSORS
# =====================================================
@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = (
        'nom',
        'type_sponsor',
        'nationalite',
        'telephone',
        'email',
    )

    list_filter = (
        'type_sponsor',
        'nationalite',
    )

    search_fields = (
        'nom',
        'telephone',
        'email',
    )


# =====================================================
# 🧩 INTERMEDIAIRES
# =====================================================
@admin.register(Intermediaire)
class IntermediaireAdmin(admin.ModelAdmin):
    list_display = (
        'nom',
        'organisation',
        'telephone',
        'email',
    )

    search_fields = (
        'nom',
        'telephone',
        'email',
        'organisation',
    )


# =====================================================
# 🔗 PARRAINAGES
# =====================================================
@admin.register(Parrainage)
class ParrainageAdmin(admin.ModelAdmin):
    list_display = (
        'orphelin',
        'sponsor',
        'type_kafala',
        'montant_mru',
        'montant_devise',
        'solde',
        'statut',
        'date_debut',
        'date_fin',
    )

    list_filter = (
        'type_kafala',
        'statut',
    )

    search_fields = (
        'orphelin__nom_complet',
        'orphelin__code',
        'orphelin__nni',
        'orphelin__nom_tuteur',
        'orphelin__telephone_tuteur',
        'sponsor__nom',

    )

    autocomplete_fields = (
        'orphelin',
        'sponsor',
        'intermediaire',
    )


# =====================================================
# 💰 TRANSACTIONS FINANCIERES
# =====================================================
@admin.register(TransactionFinanciere)
class TransactionFinanciereAdmin(admin.ModelAdmin):
    list_display = (
        'type_transaction',
        'montant',
        'parrainage',
        'cree_par',
        'date_creation',
    )

    list_filter = (
        'type_transaction',
        'date_creation',
    )

    search_fields = (
        'description',
    )

    readonly_fields = (
        'date_creation',
    )


# =====================================================
# 🧾 JOURNAL AUDIT
# =====================================================
@admin.register(JournalAudit)
class JournalAuditAdmin(admin.ModelAdmin):
    list_display = (
        'utilisateur',
        'action',
        'modele',
        'objet_id',
        'date_action',
    )

    list_filter = (
        'modele',
        'date_action',
    )

    readonly_fields = (
        'utilisateur',
        'action',
        'modele',
        'objet_id',
        'date_action',
    )


# =====================================================
# ⚙️ ADMIN CONFIG
# =====================================================
admin.site.site_header = "نظام تسيير كفالة الأيتام"
admin.site.site_title = "إدارة جمعية التضامن"
admin.site.index_title = "لوحة التحكم"
