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
        #TODO testen ob das so klappt mit dem zählen
        tmp_form = form_class()
        for field_name in tmp_form.fields.keys():
            db_field = get_db_field_name(field_name)
            field_type = tmp_form.fields[field_name]
            if hasattr(user, db_field):
                total_fields += 1
                value = getattr(user, db_field)
                
                # Check if field is filled
                is_filled = False
                if isinstance(field_type, forms.ChoiceField):
                    # Für ChoiceField: Wert ist nur ausgefüllt, wenn er nicht leer ist 
                    # und nicht der Standard-Text "Choisissez un élément." ist
                    if value and value != '' and value != 'Choisissez un élément.':
                        is_filled = True
                elif isinstance(field_type, forms.BooleanField):
                    # Für BooleanField: Wert ist ausgefüllt, wenn er True ist
                    is_filled = bool(value)
                elif isinstance(field_type, forms.ImageField):
                    # Für ImageField: Wert ist ausgefüllt, wenn ein Bild vorhanden ist
                    is_filled = bool(value)
                else:
                    # Für andere Felder: Wert ist ausgefüllt, wenn er nicht leer ist
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
    
