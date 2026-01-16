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
'''
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
        # 'code',
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
'''

@admin.register(Orphelin)
class OrphelinAdmin(admin.ModelAdmin):

    # ======= ما يظهر في القائمة =======
    list_display = (
        "code",
        "nom_complet",
        "nni",
        "genre",
        "scolarite",
        "statut",
        "statut_verification",
        "afficher_photo",
        "date_creation",
    )

    # ======= البحث =======
    search_fields = (
        "code",
        "nom_complet",
        "nni",
        "nom_tuteur",
        "telephone_tuteur",
        "nom_ecole",
    )

    # ======= الفلاتر الجانبية =======
    list_filter = (
        "statut",
        "statut_verification",
        "nature_orphelin",
        "genre",
        "scolarite",
        "niveau_social",
        "etat_mere",
        "type_logement",
        "date_creation",
    )

    # ======= الترتيب الافتراضي =======
    ordering = ("-date_creation",)

    # ======= التقسيم داخل صفحة التفاصيل =======
    fieldsets = (
        ("📌 معلومات الهوية", {
            "fields": ("code", "nom_complet", "nni", "genre", "date_naissance", "nature_orphelin", "lien_maps")
        }),

        ("👨‍👩‍👦 الأسرة والوصي", {
            "fields": (
                "nom_tuteur", "telephone_tuteur", "adresse",
                "nom_mere", "etat_mere",
                "nombre_freres", "rang_entre_freres", "taille_famille",
                "travail_tuteur",
            )
        }),

        ("⚰️ معلومات الأب", {
            "fields": ("travail_pere", "annee_deces_pere", "cause_deces_pere"),
            "classes": ("collapse",),
        }),

        ("🏠 السكن", {
            "fields": ("type_logement", "etat_logement"),
            "classes": ("collapse",),
        }),

        ("🎓 التعليم", {
            "fields": ("scolarite", "niveau_scolaire", "classe", "nom_ecole"),
        }),

        ("🩺 الوضع الصحي والاجتماعي", {
            "fields": ("etat_sante", "niveau_social"),
        }),

        ("📂 المرفقات", {
            "fields": ("photo", "dossier_pdf"),
        }),

        ("🔐 الحالة والإدارة", {
            "fields": ("statut", "statut_verification", "cree_par", "verifie_par"),
        }),
    )

    # ======= يجعل code غير قابل للتعديل بعد الإنشاء =======
    readonly_fields = ("code", "date_creation", "afficher_photo")

    # ======= صورة مصغرة جميلة في الإدارة =======
    def afficher_photo(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" width="80" height="80" style="border-radius:8px;" />',
                obj.photo.url
            )
        return "لا توجد صورة"

    afficher_photo.short_description = "الصورة"

    # ======= حفظ المستخدم الذي أنشأ اليتيم تلقائيًا =======
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.cree_par = request.user
        super().save_model(request, obj, form, change)

    # ======= زر سريع لتفعيل التدقيق =======
    actions = ["valider_orphelins"]

    @admin.action(description="✅ تفعيل الأيتام المختارين")
    def valider_orphelins(self, request, queryset):
        queryset.update(
            statut_verification="valide",
            verifie_par=request.user
        )



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
        'montant_mois',
        'montant_devise',
        'montant_devise_mois',
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
