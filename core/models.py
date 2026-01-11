from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
from cloudinary.models import CloudinaryField

def generer_code_orphelin():
    annee = timezone.now().year
    dernier = Orphelin.objects.filter(
        code__startswith=f"ORP-{annee}"
    ).count() + 1
    return f"ORP-{annee}-{dernier:06d}"


# =====================================================
# 👤 Utilisateurs
# =====================================================

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'مدير عام'),
        ('accountant', 'محاسب'),
        ('staff', 'موظف'),
        ('field', 'مشرف ميداني'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, verbose_name="الدور")
    telephone = models.CharField(max_length=20, blank=True, null=True, verbose_name="رقم الهاتف")

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='core_users',
        blank=True,
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='core_users_permissions',
        blank=True,
        verbose_name='user permissions',
    )

    class Meta:
        verbose_name = "مستخدم"
        verbose_name_plural = "المستخدمون"


# =====================================================
# 👶 Orphelins
# =====================================================

class Orphelin(models.Model):
    GENRE_CHOICES = (('m', 'ذكر'), ('f', 'أنثى'))

    STATUT_CHOICES = (
        ('actif', 'نشط'),
        ('suspendu', 'موقوف'),
        ('archive', 'مؤرشف'),
    )

    SCOLARITE_CHOICES = (
        ('non_scolarise', 'غير متمدرس'),
        ('hors_age', 'دون سن الدراسة'),
        ('scolarise', 'متمدرس'),
    )

    code = models.CharField(max_length=20, unique=True, verbose_name="رقم اليتيم", editable=False)
    nom_complet = models.CharField(max_length=255, verbose_name="الاسم الكامل")
    nni = models.CharField(max_length=20, unique=True, verbose_name="الرقم الوطني للتعريف")
    genre = models.CharField(max_length=1, choices=GENRE_CHOICES, verbose_name="الجنس")
    date_naissance = models.DateField(verbose_name="تاريخ الميلاد")
    nom_tuteur = models.CharField(max_length=255, verbose_name="اسم الولي")
    telephone_tuteur = models.CharField(max_length=20, verbose_name="هاتف الولي")
    adresse = models.TextField(verbose_name="العنوان")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name="خط العرض")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name="خط الطول")
    scolarite = models.CharField(max_length=20, choices=SCOLARITE_CHOICES, verbose_name="حالة التمدرس")
    niveau_scolaire = models.CharField(max_length=100, blank=True, verbose_name="المستوى الدراسي")
    etat_sante = models.TextField(blank=True, verbose_name="الحالة الصحية")
    # photo = models.ImageField(upload_to='orphelins/photos/', blank=True, null=True, verbose_name="صورة اليتيم", max_length=255)
    # dossier_pdf = models.FileField(upload_to='orphelins/dossiers/', blank=True, null=True, verbose_name="ملف اليتيم (PDF)", max_length=255)

    photo = CloudinaryField(
        'photo',
        folder='orphelins/photos',
        blank=True,
        null=True
    )
    dossier_pdf = CloudinaryField(
        'dossier',
        resource_type='raw',
        folder='orphelins/dossiers',
        blank=True,
        null=True
    )
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='actif', verbose_name="وضعية اليتيم")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ التسجيل")

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generer_code_orphelin()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "يتيم"
        verbose_name_plural = "الأيتام"

    def __str__(self):
        return f"{self.code} - {self.nom_complet}"


# =====================================================
# 🤝 Sponsors
# =====================================================

class Sponsor(models.Model):
    TYPE_SPONSOR_CHOICES = (
        ('individuel', 'فرد'),
        ('organisation', 'مؤسسة'),
    )

    nom = models.CharField(max_length=255, verbose_name="اسم الكافل")
    type_sponsor = models.CharField(max_length=20, choices=TYPE_SPONSOR_CHOICES, verbose_name="نوع الكافل")
    nationalite = models.CharField(max_length=100, blank=True, verbose_name="الجنسية")
    telephone = models.CharField(max_length=20, verbose_name="الهاتف")
    email = models.EmailField(blank=True, null=True, verbose_name="البريد الإلكتروني")
    adresse = models.TextField(blank=True, verbose_name="العنوان")

    class Meta:
        verbose_name = "كافل"
        verbose_name_plural = "الكافلون"

    def __str__(self):
        return self.nom


# =====================================================
# 🧩 Intermédiaires (الوسطاء)
# =====================================================

class Intermediaire(models.Model):
    nom = models.CharField(max_length=255, verbose_name="اسم الوسيط")
    telephone = models.CharField(max_length=20, verbose_name="الهاتف")
    email = models.EmailField(blank=True, null=True, verbose_name="البريد الإلكتروني")
    organisation = models.CharField(max_length=255, blank=True, verbose_name="الجهة / المؤسسة")

    class Meta:
        verbose_name = "وسيط"
        verbose_name_plural = "الوسطاء"

    def __str__(self):
        return self.nom


# =====================================================
# 🔗 Parrainages (الكفالات)
# =====================================================

class Parrainage(models.Model):
    TYPE_KAFALA_CHOICES = (
        ('interne', 'داخلية'),
        ('externe', 'خارجية'),
    )

    STATUT_CHOICES = (
        ('active', 'سارية'),
        ('terminee', 'منتهية'),
        ('suspendue', 'معلقة'),
    )

    orphelin = models.ForeignKey(Orphelin, on_delete=models.CASCADE, verbose_name="اليتيم")
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE, verbose_name="الكافل")
    intermediaire = models.ForeignKey(Intermediaire, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="الوسيط")
    type_kafala = models.CharField(max_length=20, choices=TYPE_KAFALA_CHOICES, verbose_name="جهة الكفالة")
    montant_mru = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="مبلغ الكفالة بالأوقية")
    montant_devise = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name="المبلغ بالعملة الأجنبية")
    devise = models.CharField(max_length=10, blank=True, verbose_name="العملة")
    solde = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="الرصيد")
    date_debut = models.DateField(verbose_name="تاريخ بداية الكفالة")
    date_fin = models.DateField(blank=True, null=True, verbose_name="تاريخ نهاية الكفالة")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='active', verbose_name="الحالة")

    class Meta:
        verbose_name = "كفالة"
        verbose_name_plural = "الكفالات"
        unique_together = ('orphelin', 'sponsor')

    def __str__(self):
        return f"{self.sponsor} → {self.orphelin}"


# =====================================================
# 💰 Transactions financières
# =====================================================

class TransactionFinanciere(models.Model):
    TYPE_CHOICES = (
        ('entree', 'دخل'),
        ('sortie', 'صرف'),
    )

    type_transaction = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name="نوع العملية")
    montant = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="المبلغ")
    description = models.TextField(verbose_name="الوصف")
    parrainage = models.ForeignKey(Parrainage, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="الكفالة")
    cree_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="أنشئت بواسطة")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ العملية")

    class Meta:
        verbose_name = "عملية مالية"
        verbose_name_plural = "العمليات المالية"


# =====================================================
# 🧾 Audit Log
# =====================================================

class JournalAudit(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="المستخدم")
    action = models.CharField(max_length=255, verbose_name="الإجراء")
    modele = models.CharField(max_length=100, verbose_name="النموذج")
    objet_id = models.CharField(max_length=50, verbose_name="المعرف")
    date_action = models.DateTimeField(auto_now_add=True, verbose_name="التاريخ")

    class Meta:
        verbose_name = "سجل التدقيق"
        verbose_name_plural = "سجلات التدقيق"
