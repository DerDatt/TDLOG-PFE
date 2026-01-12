# from django.db import models

# from django.contrib.auth.hashers import make_password, check_password

# class MyUserData(models.Model):
#     username = models.CharField(max_length=150, unique=True)
#     password = models.CharField(max_length=256)  # gehashed

#     def set_password(self, raw_password):
#         self.password = make_password(raw_password)
#         self.save()

#     def check_password(self, raw_password):
#         return check_password(raw_password, self.password)



from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Username ist erforderlich')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    """Custom User Model"""
    
    # --- System-Felder (für Django Auth) ---
    username = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    Departement_Enseignement = models.CharField(max_length=100, default='not_chosen')
    Prenom_NOM = models.CharField(max_length=255, blank=True)
    Adresse_mail_permanente = models.CharField(max_length=255, blank=True)
    Statut_etudiant_entrepreneur = models.CharField(max_length=255, blank=True)
    Profil = models.CharField(max_length=255, blank=True)
    Double_diplome = models.CharField(max_length=255, blank=True)
    Titre_parcours_3A = models.CharField(max_length=255, blank=True)
    Etablissement_formation_3A = models.CharField(max_length=255, blank=True)
    Promotion = models.CharField(max_length=255, blank=True)
    Photo_portrait = models.CharField(max_length=255, blank=True)
    Type_de_PFE = models.CharField(max_length=255, blank=True)
    Organisme_du_PFE = models.CharField(max_length=255, blank=True)
    Type_organisme_accueil = models.CharField(max_length=255, blank=True)
    Tuteur_professionnel = models.CharField(max_length=255, blank=True)
    Fonction_tuteur_professionnel = models.CharField(max_length=255, blank=True)
    Tuteur_academique = models.CharField(max_length=255, blank=True)
    Fonction_tuteur_academique = models.CharField(max_length=255, blank=True)
    Organisme_rattachement_tuteur_academique = models.CharField(max_length=255, blank=True)
    Langue_de_redaction = models.CharField(max_length=255, blank=True)
    Si_PFE_Non_confidentiel = models.BooleanField(default=False)
    Si_PFE_Confidentiel = models.BooleanField(default=False)
    Duree_de_confidentialite = models.CharField(max_length=255, blank=True)
    Titre_PFE_FR = models.CharField(max_length=255, blank=True)
    Thematique_principale = models.CharField(max_length=255, blank=True)
    Mots_cles_FR = models.CharField(max_length=255, blank=True)
    Presentation_contexte_FR = models.CharField(max_length=255, blank=True)
    Presentation_missions_FR = models.CharField(max_length=255, blank=True)
    Resume_FR = models.CharField(max_length=255, blank=True)
    Titre_PFE_EN = models.CharField(max_length=255, blank=True)
    Mots_cles_EN = models.CharField(max_length=255, blank=True)
    Presentation_contexte_EN = models.CharField(max_length=255, blank=True)
    Presentation_missions_EN = models.CharField(max_length=255, blank=True)
    Resume_EN = models.CharField(max_length=255, blank=True)
    Bibliographie1 = models.CharField(max_length=255, blank=True)
    Bibliographie2 = models.CharField(max_length=255, blank=True)
    Bibliographie3 = models.CharField(max_length=255, blank=True)
    Nom_Image_associee = models.CharField(max_length=255, blank=True)
    Legende = models.CharField(max_length=255, blank=True)
    Nom_Du_Photographe = models.CharField(max_length=255, blank=True)
    CHECK_1 = models.BooleanField(default=False)
    CHECK_2 = models.BooleanField(default=False)
    CHECK_3 = models.BooleanField(default=False)
    
    # Django Auth Konfiguration
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []  # Beim createsuperuser abgefragte Felder (außer username & password)
    
    objects = MyUserManager()
    
    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'users'  # Gleicher Tabellenname wie in SQLAlchemy
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'