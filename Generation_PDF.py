import bcrypt
from sqlalchemy import create_engine, Column, Integer, String, Boolean, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError

# Configuration de la base de données SQLite
ENGINE = create_engine("sqlite:///users_pfe.db") # J'ai renommé le fichier pour ce nouveau projet
Base = declarative_base()
Session = sessionmaker(bind=ENGINE)

class User(Base):
    __tablename__ = 'users'

    # --- Champs Système ---
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False) # Identifiant
    hashed_password = Column(String, nullable=False)       # Mot de passe sécurisé

    # --- Champs Étudiant & Administratif ---
    # choice_field (GCC, IMI, SEGF, GI...)
    departement_enseignement = Column(String) 
    prenom_nom = Column(String)
    adresse_mail_permanente = Column(String)
    statut_etudiant_entrepreneur = Column(String)
    profil = Column(String)
    double_diplome = Column(String)
    titre_parcours_3a = Column(String)
    etablissement_formation_3a = Column(String)
    promotion = Column(String)
    photo_portrait = Column(String) # On stockera le chemin du fichier ou l'URL

    # --- Champs Tuteurs & Organisme ---
    type_de_pfe = Column(String)
    organisme_du_pfe = Column(String)
    type_organisme_accueil = Column(String)
    tuteur_professionnel = Column(String)
    fonction_tuteur_professionnel = Column(String)
    tuteur_academique = Column(String)
    fonction_tuteur_academique = Column(String)
    organisme_rattachement_tuteur_academique = Column(String)
    
    # --- Champs Détails PFE ---
    langue_de_redaction = Column(String)
    
    # Checkboxes (Boolean)
    si_pfe_non_confidentiel = Column(Boolean, default=False)
    si_pfe_confidentiel = Column(Boolean, default=False)
    
    duree_de_confidentialite = Column(String)

    # --- Contenu FR (String pour les champs longs) ---
    titre_pfe_fr = Column(String)
    thematique_principale = Column(String)
    mots_cles_fr = Column(String)
    presentation_conStringe_fr = Column(String) 
    presentation_missions_fr = Column(String)
    resume_fr = Column(String)

    # --- Contenu EN ---
    titre_pfe_en = Column(String)
    mots_cles_en = Column(String)
    presentation_conStringe_en = Column(String)
    presentation_missions_en = Column(String)
    resume_en = Column(String)

    # --- Bibliographie & Images ---
    bibliographie1 = Column(String) # String car une biblio peut être longue
    bibliographie2 = Column(String)
    bibliographie3 = Column(String)
    nom_image_associee = Column(String)
    legende = Column(String)
    nom_du_photographe = Column(String)

    # --- Checks finaux ---
    check_1 = Column(Boolean, default=False)
    check_2 = Column(Boolean, default=False)
    check_3 = Column(Boolean, default=False)

    def to_dict(self) -> dict:
        def bool_to_box(value: bool) -> str:
            return "$\\CheckedBox$" if value else "$\\Box$"
        dico =  {
        "__Departement_Enseignement__": self.departement_enseignement,
        "__Prenom_NOM__": self.prenom_nom,
        "__Adresse_mail_permanente__": self.adresse_mail_permanente,
        "__Statut_etudiant_entrepreneur__": self.statut_etudiant_entrepreneur,
        "__Profil__": self.profil,
        "__Double_diplome__": self.double_diplome,
        "__Titre_parcours_3A__": self.titre_parcours_3a,
        "__Etablissement_formation_3A__": self.etablissement_formation_3a,
        "__Promotion__": self.promotion,
        "__Photo_portrait__": self.photo_portrait,
        "__Type_de_PFE__": self.type_de_pfe,
        "__Organisme_du_PFE__": self.organisme_du_pfe,
        "__Type_organisme_accueil__": self.type_organisme_accueil,
        "__Tuteur_professionnel__": self.tuteur_professionnel,
        "__Fonction_tuteur_professionnel__": self.fonction_tuteur_professionnel,
        "__Tuteur_academique__": self.tuteur_academique,
        "__Fonction_tuteur_academique__": self.fonction_tuteur_academique,
        "__Organisme_rattachement_tuteur_academique__": self.organisme_rattachement_tuteur_academique,
        "__Langue_de_redaction__": self.langue_de_redaction,
        "__Si_PFE_Non_confidentiel__":bool_to_box(self.si_pfe_non_confidentiel),
        "__Si_PFE_Confidentiel__": bool_to_box(self.si_pfe_confidentiel),
        "__Duree_de_confidentialite__": self.duree_de_confidentialite,
        "__Titre_PFE_FR__": self.titre_pfe_fr,
        "__Thematique_principale__": self.thematique_principale,
        "__Mots_cles_FR__": self.mots_cles_fr,
        "__Presentation_contexte_FR__": self.presentation_conStringe_fr,  # champ DB existant (typo)
        "__Presentation_missions_FR__": self.presentation_missions_fr,
        "__Resume_FR__": self.resume_fr,
        "__Titre_PFE_EN__": self.titre_pfe_en,
        "__Mots_cles_EN__": self.mots_cles_en,
        "__Presentation_contexte_EN__": self.presentation_conStringe_en,  # champ DB existant (typo)
        "__Presentation_missions_EN__": self.presentation_missions_en,
        "__Resume_EN__": self.resume_en,
        "__Bibliographie1__": self.bibliographie1,
        "__Bibliographie2__": self.bibliographie2,
        "__Bibliographie3__": self.bibliographie3,
        "__Nom_Image_associee__": self.nom_image_associee,
        "__Legende__": self.legende,
        "__Nom_Du_Photographe__": self.nom_du_photographe,
        "__CHECK_1__": bool_to_box(self.check_1),
        "__CHECK_2__": bool_to_box(self.check_2),
        "__CHECK_3__": bool_to_box(self.check_3),
        }
        return dico

    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.hashed_password.encode('utf-8'))

def init_db():
    Base.metadata.create_all(ENGINE)
    print("Base de données initialisée avec le nouveau schéma PFE.")
def add_example_student():
    init_db() # S'assurer que la table existe
    session = Session()

    # Vérifier si l'exemple existe déjà pour éviter les doublons
    if session.query(User).filter_by(username='etudiant1').first():
        print("L'utilisateur existe déjà.")
        session.close()
        return

    hashed_pw = User.hash_password("monMotDePasseSuperSecurise")

    student = User(
        # Identifiants système
        username="etudiant1",
        hashed_password=hashed_pw,

        # Données personnelles
        departement_enseignement="IMI",
        prenom_nom="Jean Dupont",
        adresse_mail_permanente="jean.dupont@email.com",
        statut_etudiant_entrepreneur="Non",
        promotion="2024",
        
        # Données PFE
        titre_pfe_fr="Implémentation d'IA en milieu industriel",
        titre_pfe_en="AI Implementation in Industrial Environment",
        organisme_du_pfe="Thales",
        tuteur_academique="M. Professeur",
        
        # Textes longs
        resume_fr="Ceci est un résumé détaillé du projet de fin d'études...",
        presentation_missions_fr="1. Analyser les données.\n2. Créer le modèle.",
        
        # Booleans (Checkboxes)
        si_pfe_confidentiel=True,
        check_1=True,
        check_2=True
    )

    session.add(student)
    session.commit()
    print("Étudiant exemple ajouté avec succès !")
    session.close()

def placeholders_dict_to_user_dict(data: dict) -> dict:
    """
    Convertit un dictionnaire à clés __PLACEHOLDER__ (formulaire / LaTeX)
    vers un dictionnaire à clés = noms des colonnes SQLAlchemy de User.
    """
    return {
        # --- Étudiant & Administratif ---
        "departement_enseignement": data.get("__Departement_Enseignement__"),
        "prenom_nom": data.get("__Prenom_NOM__"),
        "adresse_mail_permanente": data.get("__Adresse_mail_permanente__"),
        "statut_etudiant_entrepreneur": data.get("__Statut_etudiant_entrepreneur__"),
        "profil": data.get("__Profil__"),
        "double_diplome": data.get("__Double_diplome__"),
        "titre_parcours_3a": data.get("__Titre_parcours_3A__"),
        "etablissement_formation_3a": data.get("__Etablissement_formation_3A__"),
        "promotion": data.get("__Promotion__"),
        "photo_portrait": data.get("__Photo_portrait__"),

        # --- Tuteurs & Organisme ---
        "type_de_pfe": data.get("__Type_de_PFE__"),
        "organisme_du_pfe": data.get("__Organisme_du_PFE__"),
        "type_organisme_accueil": data.get("__Type_organisme_accueil__"),
        "tuteur_professionnel": data.get("__Tuteur_professionnel__"),
        "fonction_tuteur_professionnel": data.get("__Fonction_tuteur_professionnel__"),
        "tuteur_academique": data.get("__Tuteur_academique__"),
        "fonction_tuteur_academique": data.get("__Fonction_tuteur_academique__"),
        "organisme_rattachement_tuteur_academique": data.get(
            "__Organisme_rattachement_tuteur_academique__"
        ),

        # --- Détails PFE ---
        "langue_de_redaction": data.get("__Langue_de_redaction__"),
        "si_pfe_non_confidentiel": bool(data.get("__Si_PFE_Non_confidentiel__")),
        "si_pfe_confidentiel": bool(data.get("__Si_PFE_Confidentiel__")),
        "duree_de_confidentialite": data.get("__Duree_de_confidentialite__"),

        # --- Contenu FR ---
        "titre_pfe_fr": data.get("__Titre_PFE_FR__"),
        "thematique_principale": data.get("__Thematique_principale__"),
        "mots_cles_fr": data.get("__Mots_cles_FR__"),
        "presentation_conStringe_fr": data.get("__Presentation_contexte_FR__"),
        "presentation_missions_fr": data.get("__Presentation_missions_FR__"),
        "resume_fr": data.get("__Resume_FR__"),

        # --- Contenu EN ---
        "titre_pfe_en": data.get("__Titre_PFE_EN__"),
        "mots_cles_en": data.get("__Mots_cles_EN__"),
        "presentation_conStringe_en": data.get("__Presentation_contexte_EN__"),
        "presentation_missions_en": data.get("__Presentation_missions_EN__"),
        "resume_en": data.get("__Resume_EN__"),

        # --- Bibliographie & Images ---
        "bibliographie1": data.get("__Bibliographie1__"),
        "bibliographie2": data.get("__Bibliographie2__"),
        "bibliographie3": data.get("__Bibliographie3__"),
        "nom_image_associee": data.get("__Nom_Image_associee__"),
        "legende": data.get("__Legende__"),
        "nom_du_photographe": data.get("__Nom_Du_Photographe__"),

        # --- Checks finaux ---
        "check_1": bool(data.get("__CHECK_1__")),
        "check_2": bool(data.get("__CHECK_2__")),
        "check_3": bool(data.get("__CHECK_3__")),
    }

def authenticate_user(username: str, password: str) -> dict or None:
    session = Session()
    try:
        user = session.query(User).filter_by(username=username).first()

        if user and user.check_password(password):
            print(f"Connexion réussie pour : {user.prenom_nom}")
            # La magie opère ici : on récupère tout le dictionnaire automatiquement
            return user.to_dict()
        
        return None

    except Exception as e:
        print(f"Erreur : {e}")
        return None
    finally:
        session.close()

def update_user_data(user_id: int, raw_data: dict) -> bool:
    """
    Met à jour les informations d'un utilisateur à partir d'un dictionnaire.
    
    Args:
        user_id (int): L'ID de l'utilisateur à modifier.
        data (dict): Dictionnaire contenant les noms des colonnes et les nouvelles valeurs.
                     Ex: {'prenom_nom': 'Nouveau Nom', 'si_pfe_confidentiel': True}
    
    Returns:
        bool: True si la mise à jour a réussi, False sinon.
    """
    session = Session()
    try:
        # 1. Récupérer l'utilisateur
        user = session.query(User).filter_by(id=user_id).first()
        
        if not user:
            print(f"Erreur : Utilisateur avec l'ID {user_id} introuvable.")
            return False

        # 2. Obtenir la liste des colonnes valides de la table User
        # Cela évite de planter si le dictionnaire contient une clé qui n'existe pas en base
        data = placeholders_dict_to_user_dict(raw_data)
        valid_columns = {c.name for c in User.__table__.columns}

        # 3. Itérer sur le dictionnaire et mettre à jour les champs
        for key, value in data.items():
            
            # Sécurité : On ne touche pas à l'ID (clé primaire)
            if key == 'id':
                continue
            
            # Cas particulier : Si on veut mettre à jour le mot de passe via cette fonction
            # Il faut penser à le hacher à nouveau !
            if key == 'password': 
                hashed = User.hash_password(value)
                setattr(user, 'hashed_password', hashed)
                continue
            
            # Mise à jour dynamique des autres champs
            if key in valid_columns:
                setattr(user, key, value)
            else:
                # Optionnel : Avertir si une clé du dico ne correspond à rien
                # print(f"Attention : La clé '{key}' n'existe pas dans la base de données. Ignorée.")
                pass

        # 4. Sauvegarder les modifications
        session.commit()
        print(f"Mise à jour réussie pour l'utilisateur ID {user_id}.")
        return True

    except Exception as e:
        session.rollback() # Annuler en cas d'erreur
        print(f"Erreur lors de la mise à jour : {e}")
        return False
    finally:
        session.close()

def create_user(user_data: dict) -> int or None:
    """
    Crée une nouvelle ligne (un nouvel utilisateur) dans la base de données.
    
    Args:
        user_data (dict): Dictionnaire contenant les données. 
                          Doit impérativement contenir 'username' et 'password'.
    
    Returns:
        int: L'ID du nouvel utilisateur si succès.
        None: Si échec (ex: identifiant déjà pris, données manquantes).
    """
    session = Session()
    try:
        # 1. Vérification des champs obligatoires pour la création
        if 'username' not in user_data or 'password' not in user_data:
            print("Erreur : 'username' et 'password' sont obligatoires.")
            return None

        # 2. Préparation des données
        # On fait une copie pour ne pas modifier le dictionnaire original de l'appelant
        data_to_insert = placeholders_dict_to_user_dict(user_data)
        
        # Gestion spécifique du mot de passe (Hachage)
        raw_password = user_data['password'] 
        data_to_insert['hashed_password'] = User.hash_password(raw_password)
        data_to_insert['username'] = user_data['username'] # On remet l'username

        # 3. Nettoyage : On ne garde que les clés qui correspondent aux colonnes de la table
        # (Pour éviter une erreur si le dict contient 'confirm_password' ou autre chose inutile)
        valid_columns = {c.name for c in User.__table__.columns}
        clean_data = {k: v for k, v in data_to_insert.items() if k in valid_columns}

        # 4. Création de l'objet User avec le "Dictionary Unpacking" (**)
        # Cela transforme {'username': 'toto', 'age': 20} en User(username='toto', age=20)
        new_user = User(**clean_data)

        # 5. Ajout et sauvegarde
        session.add(new_user)
        session.commit()
        
        print(f"Utilisateur '{new_user.username}' créé avec succès (ID: {new_user.id}).")
        return new_user.id

    except IntegrityError:
        session.rollback()
        print(f"Erreur : L'identifiant '{user_data.get('username')}' existe déjà.")
        return None
    except Exception as e:
        session.rollback()
        print(f"Erreur technique lors de la création : {e}")
        return None
    finally:
        session.close()

if __name__ == "__main__":
    session = Session()
    init_db()
    
    ##Ajouter un étudiant d'exemple
    add_example_student()

    ##Tester l'authentification et la récupération des données
    data = authenticate_user("etudiant1", "monMotDePasseSuperSecurise")
    print(data)
        
        ##Tester la mise à jour des données
        # Supposons qu'on a authentifié l'étudiant et qu'on connaît son ID (ex: 1)
    mon_user_id = 1
    
    # Dictionnaire reçu depuis le formulaire Web (Django)
    nouvelles_donnees = {
        "titre_pfe_en": "Deep Learning for Space Analysis",
        "resume_fr": "Mon résumé a changé, voici la nouvelle version...",
        "si_pfe_confidentiel": False,
        "check_1": True,
        "champ_qui_n_existe_pas": "Cette valeur sera ignorée" 
    }

    # Appel de la fonction de mise à jour
    succes = update_user_data(mon_user_id, nouvelles_donnees)

    # Vérification
    if succes:
        session = Session()
        u = session.query(User).get(mon_user_id)
        print(f"Nouveau titre EN en base : {u.titre_pfe_en}")
        session.close()
        
    ##
    ##Tester la création d'un nouvel utilisateur
    # Données reçues (simulées)
    contexte = "13 caractères" * 16  # 208 caractères
    objectifs = "13 caractères" * 20  # 260 caractères
    resume =  "13 caractères" * 100  # 1300 caractères

    contexte_en = "13 caractères" * 16  # 208 caractères
    objectifs_en = "13 caractères" * 20  # 260 caractères
    resume_en =  "13 caractères" * 100  # 1300 caractères
    nouvel_etudiant = {"username": "etudiant2",
        "password": "motDePasseUltraSecurise",
        "__Departement_Enseignement__": "Génie Civil",
        "__Prenom_NOM__": "Vincent CANNIBALO",
        "__Adresse_mail_permanente__": "Vincent.Cannizzaro@example.com",
        "__Statut_etudiant_entrepreneur__": "$\\Box$",
        "__Profil__": "Voie classique",
        "__Double_diplome__": "Université X, Ville Y, Pays Z",
        "__Titre_parcours_3A__": "Master en Transport",
        "__Etablissement_formation_3A__": "Université X, Ville Y, Pays Z",
        '__Promotion__' : '2023',
        "__Photo_portrait__": "photo.jpg",  # fichier qui doit exister !
        "__Type_de_PFE__": "Recherche",
        "__Organisme_du_PFE__": "Entreprise ABC",
        "__Type_organisme_accueil__": "Industrie",
        '__Tuteur_professionnel__' : 'Marie DURAND',
        "__Fonction_tuteur_professionnel__": "Ingénieure R\\&D",
        '__Tuteur_academique__' : 'Luc MARTIN',
        "__Fonction_tuteur_academique__": "Maître de conférences",
        "__Organisme_rattachement_tuteur_academique__": "ENPC",
        "__Langue_de_redaction__": "Français",
        "__Si_PFE_Non_confidentiel__": "Oui – autorisation de diffusion donnée.",
        "__Si_PFE_Confidentiel__": "$\\Box$",
        "__Duree_de_confidentialite__": "0 mois",
        '__Titre_PFE_FR__' : 'Mon PFE génial',
        "__Thematique_principale__": "Transport",
        '__Mots_cles_FR__' : 'super; pfe; intéressant',
        '__Presentation_contexte_FR__' : contexte,
        '__Presentation_missions_FR__' : objectifs,
        "__Resume_FR__" : resume,
        '__Titre_PFE_EN__' : 'Mon PFE cool',
        '__Mots_cles_EN__' : 'super; pfe; intéressant;génial',
        '__Presentation_contexte_EN__' : contexte_en,
        '__Presentation_missions_EN__' : objectifs_en,
        "__Resume_EN__" : resume_en,
        "__Bibliographie1__": "Réf.1",
        "__Bibliographie2__":"Réf.2",
        "__Bibliographie3__":"Réf.3",
        "__Nom_Image_associee__": "image.jpg",
        "__Legende__": "Legende de l'image",
        "__Nom_Du_Photographe__": "Meow",
        "__CHECK_1__": "$\\CheckedBox$",
        "__CHECK_2__": "$\\CheckedBox$",
        "__CHECK_3__": "$\\CheckedBox$"
    }
    

    # Appel de la fonction
    new_id = create_user(nouvel_etudiant)

    if new_id:
        print(f"L'étudiant a été enregistré sous l'index {new_id}")
    else:
        print("L'enregistrement a échoué.")
    session.close()