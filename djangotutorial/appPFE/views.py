import os
from django import forms
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import generic
# from .forms import ContactForm, DocumentForm
from .models import WholeDocument #, LoginForm
from auto_translation.Traducteur import traduire_fr_en, traduire_fr_en_dummy
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage

from .utils import strip_name_of_underscores_begin_end, add_underscored_to_name_begin_end

def index(request):
    return HttpResponse("This here is the index of our () PFE (Projet final etudes or similar lol). ")

class IndexView(generic.ListView):
    template_name = "appPFE/index.html"
    # context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return HttpResponse("dsdsasadsasdasadsadsad ")

# class DocView(generic.FormView): 
#     template_name = "appPFE/document_form.html"
#     form_class = DocumentForm
#     success_url = "/success/"

#     def form_valid(self, form):
#         # hier kannst du speichern, mail senden, loggen usw.
#         print(form.cleaned_data)
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = "Dokument ausfüllen"
#         return context

#     def get_success_url(self):
#         return reverse("success_page")


# class ContactFormView(generic.edit.FormView):
#     template_name = "appPFE/contact.html"
#     form_class = ContactForm
#     success_url = "/danke/"

#     def form_valid(self, form):
#         form.save()   # Bei ModelForm: Speichert in DB
#         return super().form_valid(form)

# def login_view(request):
#     if request.method == "POST":
#         form = LoginForm(request.POST, request.FILES) #, path_csv = path)
#         if form.is_valid():
#             form.save()

#             # login successfull => send to doc_form
#             return redirect("appPFE:docForm")
#         else: 
#             print("Not Valid")
#     else:
#         form = LoginForm() 

#     return render(request, "appPFE/login_form.html", {"form": form})


# TODO: move to utils: 
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
    
    Returns: None if successful, Form with errors if validation failed
    """
    if validate:
        form = form_class(post_data, files)
        if not form.is_valid():
            return form  # Return form with errors
    
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
    return None  # Success

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


def doc_view(request):
    if request.method == "POST":
        action = request.POST.get('action')
        
        if action == 'save':
            # SAVE: without validation
            save_form_data_to_user(
                request.user, 
                WholeDocument, 
                request.POST, 
                request.FILES, 
                validate=False
            )
            return redirect("appPFE:docForm")
        
        elif action == 'send':
            # SEND: with validation
            form_with_errors = save_form_data_to_user(
                request.user, 
                WholeDocument, 
                request.POST, 
                request.FILES, 
                validate=True
            )
            
            if form_with_errors:
                # Validation failed
                return render(request, "appPFE/document_form.html", {
                    "form": form_with_errors,
                    "translatable_fields": form_with_errors.autotranslatable,
                })
            
            # Success
            return redirect("appPFE:success")
    
    # GET: Pre-fill form with saved user data
    form = load_user_data_into_form(request.user, WholeDocument)
    
    # Check if new user
    is_new_user = request.session.pop('is_new_user', False)
    
    # Calculate completion stats
    stats = calculate_completion_stats(request.user, WholeDocument)
    
    context = {
        'form': form,
        'translatable_fields': form.autotranslatable,
        'is_new_user': is_new_user,
        'number_filled_fields': stats['filled_fields'],
        'number_total_fields': stats['total_fields'],
        'completion_percentage': stats['completion_percentage'],
    }
    
    return render(request, "appPFE/document_form.html", context)


# @login_required
# def doc_view(request):
#     if request.method == "POST":
#         # Prüfe welcher Button geklickt wurde
#         action = request.POST.get('action')
        
#         if action == 'save':
#             # SAVE: Speichern OHNE Validierung (auch bei leeren Feldern)
#             user = request.user
#             tmp_form = WholeDocument()
#             # print("=== DEBUG SAVE ===")
#             # print("Form-Felder:", WholeDocument().fields.keys())
#             # print("POST-Daten:", request.POST.keys())
#             # print("User-Attribute:", [field.name for field in user._meta.get_fields()])


#             # Direkt aus POST-Daten lesen (ohne Form-Validierung)
#             for field_name, field in tmp_form.fields.items():

#                 if isinstance(field, forms.BooleanField):
#                     # Checkbox: True if in POST, else False
#                     value = field_name in request.POST
#                     name_in_db = get_db_field_name(field_name)
#                     if hasattr(user, name_in_db):
#                         setattr(user, name_in_db, value)
                        
#                 elif isinstance(field, forms.ImageField):
#                     # Image/File fields: Prüfe ob neues Bild hochgeladen wurde
#                     name_in_db = get_db_field_name(field_name)
                    
#                     # Prüfe ob "clear" Checkbox aktiviert ist
#                     clear_checkbox_name = f"{field_name}-clear"
#                     should_clear = clear_checkbox_name in request.POST
                    
#                     if should_clear:
#                         # Bild löschen wenn Checkbox aktiviert
#                         if hasattr(user, name_in_db):
#                             old_file = getattr(user, name_in_db)
#                             if old_file:
#                                 # Bestimme den Dateipfad (kann FileField-Objekt oder String sein)
#                                 file_path = old_file.name if hasattr(old_file, 'name') else str(old_file)
#                                 # Lösche alte Datei vom Server
#                                 if file_path and default_storage.exists(file_path):
#                                     default_storage.delete(file_path)
#                                 # Lösche aus DB
#                                 setattr(user, name_in_db, None)
#                     elif field_name in request.FILES:
#                         # Neues Bild wurde hochgeladen
#                         uploaded_file = request.FILES[field_name]
                        
#                         # Lösche altes Bild falls vorhanden
#                         if hasattr(user, name_in_db):
#                             old_file = getattr(user, name_in_db)
#                             if old_file:
#                                 # Bestimme den Dateipfad (kann FileField-Objekt oder String sein)
#                                 file_path = old_file.name if hasattr(old_file, 'name') else str(old_file)
#                                 if file_path and default_storage.exists(file_path):
#                                     default_storage.delete(file_path)
                        
#                         # Speichere neues Bild
#                         file_path = name_for_picture(user)
#                         saved_path = default_storage.save(file_path, uploaded_file)
                        
#                         # Speichere in DB: Django's ImageField kann direkt mit dem Pfad arbeiten
#                         if hasattr(user, name_in_db):
#                             # Weise die gespeicherte Datei dem ImageField zu
#                             # saved_path ist relativ zu MEDIA_ROOT
#                             setattr(user, name_in_db, saved_path)
#                     # Wenn kein neues Bild und keine Clear-Checkbox: behalte alten Wert
#                     # (nichts tun)
                    
#                 else:
#                     # non-checkbox, non-image fields
#                     value = request.POST.get(field_name, '')
#                     name_in_db = get_db_field_name(field_name)
#                     if hasattr(user, name_in_db):
#                         setattr(user, name_in_db, value)

#             user.save()
#             # messages.success(request, "Daten gespeichert!")
#             return redirect("appPFE:docForm")
            
#         elif action == 'send':
#             # SEND: MIT Validierung (alle Pflichtfelder müssen ausgefüllt sein)
#             form = WholeDocument(request.POST, request.FILES)
#             user = request.user

#             if form.is_valid():
#                 document = form.save() #commit=False)
#                 document.user = request.user
#                 print("test")
#                 document.save()

#                 # save image in media/images
#                 for field_name, field_value in request.FILES.items():
#                         from django.core.files.storage import default_storage
                        
#                         file_name = f"{request.user.id}_{field_name}.png"
#                         file_path = os.path.join('images', file_name)
#                         default_storage.save(file_path, field_value)

                        
#                         field_name_without_underscored = get_db_field_name(field_name)
#                         if hasattr(user, field_name_without_underscored):
#                             setattr(user, field_name_without_underscored, saved_path)
#             # else: 
#             #     return render(request, "appPFE/document_form.html", {
#             #         "form": form,
#             #         "translatable_fields": form.autotranslatable,
#             #     })

#             user.save()
#             # return redirect("appPFE:success")
    
#     else:
#         # GET: Form mit gespeicherten User-Daten vorausfüllen
#         initial_data = {}
#         if request.user.is_authenticated:
#             for field_name in WholeDocument().fields.keys():
#                 # name_with_underscored = add_underscored_to_name_begin_end(field_name)
#                 name_in_db = get_db_field_name(field_name)

#                 if(name_in_db == "Photo_portrait"): 
#                     print(name_in_db, "in loading from db")
#                     if hasattr(request.user, name_in_db):
#                         value = getattr(request.user, name_in_db)
#                         print(value)
#                         print(bool(value))

#                 if hasattr(request.user, name_in_db):
#                     value = getattr(request.user, name_in_db)
#                     if value:  # Nur wenn Wert vorhanden
#                         initial_data[field_name] = value
        
#         form = WholeDocument(initial=initial_data)
    
#     # Checke ob neuer User
#     is_new_user = request.session.pop('is_new_user', False)
    
#     # Zähle ausgefüllte Felder
#     number_filled_fields = 0
#     number_total_fields = 0
    
#     if request.user.is_authenticated:
#         for field_name in WholeDocument().fields.keys():
#             field_name_without_underscored = get_db_field_name(field_name)
#             if hasattr(request.user, field_name_without_underscored):
#                 number_total_fields += 1
#                 value = getattr(request.user, field_name_without_underscored)
#                 # Check ob Feld ausgefüllt ist
#                 if value and value != '':
#                     number_filled_fields += 1
    
#     # Prozentsatz berechnen
#     if number_total_fields > 0:
#         completion_percentage = int((number_filled_fields / number_total_fields) * 100)
#     else:
#         completion_percentage = 0
    
#     context = {
#         'form': form,
#         'translatable_fields': form.autotranslatable,
#         'is_new_user': is_new_user,
#         'number_filled_fields': number_filled_fields,
#         'number_total_fields': number_total_fields,
#         'completion_percentage': completion_percentage,  # ← NEU
#     }

#     return render(request, "appPFE/document_form.html", context)

def translate_view(request):
    # Get ALL GET parameters
    # Assumption: Exactly ONE field pair is provided
    
    # Find the source parameter (the one with content)
    source_param = None
    source_text = None
    
    for key, value in request.GET.items():
        if value:  # Only parameters with a value
            source_param = key
            source_text = value
            break
    
    if not source_text:
        return JsonResponse({'error': 'No text to translate'}, status=400)
    
    # Translate the text
    translated_text = traduire_fr_en(source_text)
    
    # Determine the target parameter
    # Assumption: _FR_ becomes _EN_
    target_param = source_param.replace('_FR_', '_EN_')
    
    return JsonResponse({target_param: translated_text})


# def translate_view(request):
#     fr_text = request.GET.get('__Presentation_contexte_FR__', '')
#     # en_text = traduire_fr_en_dummy(fr_text)
#     en_text = traduire_fr_en(fr_text)
#     return JsonResponse({'__Presentation_contexte_EN__': en_text})

# def contact_view(request):
#     if request.method == "POST":
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("contact_success")
#     else:
#         form = ContactForm()

#     return render(request, "appPFE/contact_form.html", {"form": form})


def success_view(request):
    return render(request, "appPFE/success.html")