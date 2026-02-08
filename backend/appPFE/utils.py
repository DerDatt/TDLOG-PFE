import os
from django import forms
from django.core.files.storage import default_storage

def strip_name_of_underscores_begin_end(name: str) -> str:
    # Remove underscores only at the beginning and end, not inside the string
    return name.lstrip('_').rstrip('_')

def add_underscored_to_name_begin_end(name: str) -> str:
    # adds 2 underscored before and 2 after the name
    return f"__{name}__"


def name_for_picture(user):
    """Returns the name for the picture using username and user id"""
    value = f"{user.username}_{user.id}_picture.png"
    value = os.path.join('images', value)
    return value

def get_db_field_name(form_field_name):
    """Converts form field name to database field name"""
    return strip_name_of_underscores_begin_end(form_field_name)

def delete_old_image(user, field_name):
    """Deletes old image if it exists"""
    # TODO: test if it deletes from db AND folder or only one and write in function description
    if not hasattr(user, field_name):
        return
    
    old_file = getattr(user, field_name)
    if not old_file:
        return
    
    file_path = old_file.name if hasattr(old_file, 'name') else str(old_file)
    if file_path and default_storage.exists(file_path):
        default_storage.delete(file_path)

def handle_image_field(user, field_name, post_data, files):
    """
    Handles ImageField for both SAVE and SEND
    Returns: True if something was changed
    """
    db_field = get_db_field_name(field_name)
    clear_checkbox = f"{field_name}-clear"
    
    # Case 1: Image should be deleted
    if clear_checkbox in post_data:
        delete_old_image(user, db_field)
        setattr(user, db_field, None)
        return True
    
    # Case 2: New image uploaded
    if field_name in files:
        delete_old_image(user, db_field)
        uploaded_file = files[field_name]
        file_path = name_for_picture(user)
        saved_path = default_storage.save(file_path, uploaded_file)
        setattr(user, db_field, saved_path)
        return True
    
    # Case 3: No changes
    return False


def fill_user_with_default_data(user, form_class, post_data, files):

    contexte = "13 caractères" * 16  # 208 caractères
    objectifs = "13 caractères" * 20  # 260 caractères
    resume =  "13 caractères" * 100  # 1300 caractères

    contexte_en = "13 caractères" * 16  # 208 caractères
    objectifs_en = "13 caractères" * 20  # 260 caractères
    resume_en =  "13 caractères" * 100  # 1300 caractères


    variables = {
        "__Departement_Enseignement__": "IMI",
        "__Prenom_NOM__": "Vincent CANNIZZARO",
        "__Adresse_mail_permanente__": "Vincent.Cannizzaro@example.com",
        "__Statut_etudiant_entrepreneur__": "$\\Box$",
        "__Profil__": "Voie classique",
        "__Double_diplome__": "Université X, Ville Y, Pays Z",
        "__Titre_parcours_3A__": "Master en Transport",
        "__Etablissement_formation_3A__": "Université X, Ville Y, Pays Z",
        '__Promotion__' : '2023',
        "__Photo_portrait__": "default_picture.jpg",  # fichier qui doit exister !
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

    tmp_form = form_class()
    for var_field_name, var_value in variables.items():
        db_field = get_db_field_name(var_field_name)
        
        if not hasattr(user, db_field):
            print("ERROR IN FUNCTION \"save_form_data_to_user\" (variables dict). \nUser seems not to have the attribute" + str(db_field) + ". ")
            continue

        # Finde den passenden Fieldtyp im Form
        tmp_form_field = tmp_form.fields.get(var_field_name)
        if isinstance(tmp_form_field, forms.ImageField):
            # Note: hier Annahme: Bildfelder werden ggf. separat behandelt/gesetzt
            handle_image_field(user, var_field_name, post_data, files)
        elif isinstance(tmp_form_field, forms.BooleanField):
            value = bool(var_value)
            setattr(user, db_field, value)
        else:
            value = var_value
            setattr(user, db_field, value)



def save_form_data_to_user(user, form_class, post_data, files, validate=False):
    """
    Saves form data to user object
    
    validate=False: SAVE mode (no validation)
    validate=True: SEND mode (with validation)
    
    Returns: validated_form if validate=True (or form with errors if validation failed), None if validate=False
    """
    validated_form = None
    if validate:
        validated_form = form_class(post_data, files)
        if not validated_form.is_valid():
            return validated_form  # Return form with errors
    
    # Iterate through fields
    tmp_form = form_class()
    for field_name, field in tmp_form.fields.items():
        db_field = get_db_field_name(field_name)
        
        if not hasattr(user, db_field):
            print("ERROR IN FUNCTION \"save_form_data_to_user\". \nUser seems not to have the attribute" + str(db_field) + ". ")
            continue
        
        if isinstance(field, forms.ImageField):
            handle_image_field(user, field_name, post_data, files)
        
        elif isinstance(field, forms.BooleanField):
            value = field_name in post_data
            setattr(user, db_field, value)
        
        else:
            value = post_data.get(field_name, '')
            setattr(user, db_field, value)

    # fill_user_with_default_data(user, form_class, post_data, files)

    user.save()
    return validated_form  # Return validated form if validate=True, None if validate=False

def load_user_data_into_form(user, form_class):
    """
    Loads user data into form initial values
    Returns: Form with initial data
    """
    initial_data = {}
    
    if user.is_authenticated:
        for field_name in form_class().fields.keys():
            db_field = get_db_field_name(field_name)
            
            if hasattr(user, db_field):
                value = getattr(user, db_field)
                if value:  # Only if value exists
                    initial_data[field_name] = value
    
    return form_class(initial=initial_data)

def calculate_completion_stats(user, form_class):
    """
    Calculates form completion statistics
    Returns: dict with filled_fields, total_fields, completion_percentage
    """
    filled_fields = 0
    total_fields = 0
    
    if user.is_authenticated:
        #TODO test if counting works correctly
        tmp_form = form_class()
        for field_name in tmp_form.fields.keys():
            db_field = get_db_field_name(field_name)
            field_type = tmp_form.fields[field_name]

            # Skip BooleanField fields for counting
            if isinstance(field_type, forms.BooleanField):
                continue

            if hasattr(user, db_field):
                total_fields += 1
                value = getattr(user, db_field)
                
                # Check if field is filled
                is_filled = False
                if isinstance(field_type, forms.ChoiceField):
                    # For ChoiceField: value is only filled if it's not empty
                    # and not a placeholder/default (model default 'not_chosen' or form placeholder)
                    empty_choices = ('', 'Choisissez un élément.', 'not_chosen')
                    if value and value not in empty_choices:
                        is_filled = True
                elif isinstance(field_type, forms.ImageField):
                    # For ImageField: value is filled if an image exists
                    is_filled = bool(value)
                else:
                    # For other fields: value is filled if it's not empty
                    is_filled = bool(value and value != '')
                
                if is_filled:
                    filled_fields += 1
    
    # Calculate percentage
    if total_fields > 0:
        completion_percentage = int((filled_fields / total_fields) * 100)
    else:
        completion_percentage = 0
    
    return {
        'filled_fields': filled_fields,
        'total_fields': total_fields,
        'completion_percentage': completion_percentage,
    }  
    
