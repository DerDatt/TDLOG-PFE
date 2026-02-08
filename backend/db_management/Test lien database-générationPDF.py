from Generation_PDF import *
from generate_text import *      


if __name__ == '__main__':
    session = Session()
    init_db()
    contexte = "13 caractères" * 16  # 208 caractères
    objectifs = "13 caractères" * 20  # 260 caractères
    resume =  "13 caractères" * 100  # 1300 caractères

    contexte_en = "13 caractères" * 16  # 208 caractères
    objectifs_en = "13 caractères" * 20  # 260 caractères
    resume_en =  "13 caractères" * 100  # 1300 caractères
    nouvel_etudiant = {"username": "etudiant6",
        "password": "motDePasseUltraSecurise",
        "__Departement_Enseignement__": "Génie Civil",
        "__Prenom_NOM__": "JAKOB DUPONT",
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
    new_id = create_user(nouvel_etudiant)
    print(f"Nouvel étudiant créé avec l'ID : {new_id}")
    #update_user_data(5, nouvel_etudiant)
    data = authenticate_user("etudiant6", "motDePasseUltraSecurise")

    print(data)
    #print type of data
    
    render_pdf(data)
    session.close()