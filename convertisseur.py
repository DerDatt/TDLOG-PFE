def test_nom( name: str) -> bool:
    """Vérifie que le nom est au format Prénom NOM avec les bonnes capitalisations, y compris pour les prénoms et les noms composés."""
    full_name = name.split(' ')
    if len(full_name) < 2:
        return False

    indice_nom_de_famille = 0
    for i in range(len(full_name)-1, -1, -1):
        if full_name[i][1:].islower():
            indice_nom_de_famille = i + 1
            break
    if indice_nom_de_famille == 0:
        return False
    prenoms = full_name[:indice_nom_de_famille]
    nom_de_famille = full_name[indice_nom_de_famille:]
    for prenom in prenoms:
        if not (prenom[0].isupper() and prenom[1:].islower()):
            return False
    for nom in nom_de_famille:
        if not nom.isupper():
            return False
    return True

           

def test_normes(d: dict[str, str]) -> dict[str, bool]:
    valid: dict[str, bool] = {}

    ## Vérification du format du nom de l'élève
    valid['__Prenom_NOM__'] = test_nom(d['__Prenom_NOM__'])

    ## Vérification que l'année est bien un nombre
    annee_key = '__Promotion__'
    annee = d[annee_key]
    valid[annee_key] = annee.isdigit()

    ## Vérification du format du nom du Tuteur professionnel
    tp_key = '__Tuteur_professionnel__'
    valid[tp_key] = test_nom(d[tp_key])

    ## Vérification du format du nom du Tuteur académique
    ta_key = '__Tuteur_academique__'
    valid[ta_key] = test_nom(d[ta_key])

    ## Vérification de la taille du titre du PFE
    titre_key = '__Titre_PFE_FR__'
    titrePFE = d[titre_key]
    valid[titre_key] = 10 <= len(titrePFE) <= 75

     ## Vérification des mots clés
    mots_key = '__Mots_cles_FR__'
    mots_clefs = [m.strip() for m in d[mots_key].split(';') if m.strip() != '']
    valid[mots_key] = 3 <= len(mots_clefs) <= 5
    for mot_clef in mots_clefs:
        if not mot_clef.islower():
            valid[mots_key] = False
            break

    ## Vérification de la longueur du contexte
    contexte_key = '__Presentation_contexte_FR__'
    contexte = d[contexte_key]
    valid[contexte_key] = 200 <= len(contexte) <= 450

    ## Vérification de la longueur des objectifs
    objectifs_key = '__Presentation_missions_FR__'
    objectifs = d[objectifs_key]
    valid[objectifs_key] = 200 <= len(objectifs) <= 450

    ## Vérification de la longueur du résumé
    resume_key = '__Resume_FR__'
    objectifs = d[resume_key]
    valid[resume_key] = 1150 <= len(objectifs) <= 1700

    ##De même mais en anglais

    ## Vérification de la taille du titre du PFE en anglais
    titre_key = '__Titre_PFE_EN__'
    titrePFE = d[titre_key]
    valid[titre_key] = 10 <= len(titrePFE) <= 75

     ## Vérification des mots clés en anglais
    mots_key = '__Mots_cles_EN__'
    mots_clefs = [m.strip() for m in d[mots_key].split(';') if m.strip() != '']
    valid[mots_key] = 3 <= len(mots_clefs) <= 5
    for mot_clef in mots_clefs:
        if not mot_clef.islower():
            valid[mots_key] = False
            break

    ## Vérification de la longueur du contexte en anglais
    contexte_key = '__Presentation_contexte_EN__'
    contexte = d[contexte_key]
    valid[contexte_key] = 200 <= len(contexte) <= 450

    ## Vérification de la longueur des objectifs en anglais
    objectifs_key = '__Presentation_missions_EN__'
    objectifs = d[objectifs_key]
    valid[objectifs_key] = 200 <= len(objectifs) <= 450

    ## Vérification de la longueur du résumé en anglais
    resume_key = '__Resume_EN__'
    objectifs = d[resume_key]
    valid[resume_key] = 1150 <= len(objectifs) <= 1700

    valid['__CHECK_1__'] = ( d['__CHECK_1__'] == "$\\CheckedBox$")

    valid['__CHECK_2__'] = ( d['__CHECK_2__'] == "$\\CheckedBox$")

    valid['__CHECK_3__'] = ( d['__CHECK_3__'] == "$\\CheckedBox$")



    if not (False in valid.values()):
        valid['all_valid'] = True
    else:
        valid['all_valid'] = False
    return valid

def test_key(key,value):
    match key:
        case '__Prenom_NOM__' | '__Tuteur_professionnel__'|'__Tuteur_academique__':
            if test_nom(value):
                return ""
            else:
                return "Erreur, format requis : Prénom NOM"
            
        case '__PROMOTION__' :
            if value.isdigit():
                return ""
            else:
                return "Erreur, veuillez entrer un nombre"
            
        case '__Titre_PFE_FR__' | '__Titre_PFE_EN__':
            if 10<=len(value)<=75: 
                return ""
            else :
                return "Erreur, le titre doit contenir entre 10 et 75 caractères"
            
        case '__Mots_cles_FR__' | '__Mots_cles_EN__':
            mots_clefs = [m.strip() for m in value.split(';') if m.strip() != '']
            if (3>len(mots_clefs)) or (5<len(mots_clefs)):
                return "Erreur, veuillez entrer entre 3 et 5 mots clefs"
            else:
                for mot_clef in mots_clefs:
                    if not mot_clef.islower():
                        return "Erreur, veuillez écrire vos mots clefs en miniscule"
                return ""
            
        case '__Presentation_contexte_FR__' | '__Presentation_contexte_EN__':
            if 200<=len(value)<=450: 
                return ""
            else :
                return "Erreur, le contexte doit contenir entre 200 et 450 caractères"
        
        case '__Presentation_mission_FR__' | '__Presentation_mission_EN__':
            if 200<=len(value)<=450: 
                return ""
            else :
                return "Erreur, les missions doivent contenir entre 200 et 450 caractères"
            
        case '__Resume_FR__' | '__Resume_EN__':
            if 1150<=len(value)<=1700: 
                return ""
            else :
                return "Erreur, le résumé doit contenir entre 200 et 450 caractères"
            
        case '__CHECK_1__' | '__CHECK_2__' | '__CHECK_3__':
            if not value:
                return "Erreur, veuillez cocher cette case"
            else:
                return ""
            
        

            
            
        
contexte = "13 caractères" * 16  # 208 caractères
objectifs = "13 caractères" * 20  # 260 caractères
resume =  "13 caractères" * 100  # 1300 caractères

contexte_en = "13 caractères" * 16  # 208 caractères
objectifs_en = "13 caractères" * 20  # 260 caractères
resume_en =  "13 caractères" * 100  # 1300 caractères



test = {
    "__Departement_Enseignement__": "Génie Civil",
    "__Prenom_NOM__": "Vincent CANNIZZARO",
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
print(test_normes(test))
    