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
    value = f"{user.username}_{user.id}_picture.png"
    value = os.path.join('images', value)
    return value

@login_required
def doc_view(request):
    if request.method == "POST":
        # Prüfe welcher Button geklickt wurde
        action = request.POST.get('action')
        
        if action == 'save':
            # SAVE: Speichern OHNE Validierung (auch bei leeren Feldern)
            user = request.user
            tmp_form = WholeDocument()
            # print("=== DEBUG SAVE ===")
            # print("Form-Felder:", WholeDocument().fields.keys())
            # print("POST-Daten:", request.POST.keys())
            # print("User-Attribute:", [field.name for field in user._meta.get_fields()])
            from django.core.files.storage import default_storage


            # Direkt aus POST-Daten lesen (ohne Form-Validierung)
            for field_name, field in tmp_form.fields.items():

                if isinstance(field, forms.BooleanField):
                    # Checkbox: True if in POST, else False
                    value = field_name in request.POST
                    name_in_db = strip_name_of_underscores_begin_end(field_name)
                    if hasattr(user, name_in_db):
                        setattr(user, name_in_db, value)
                        
                elif isinstance(field, forms.ImageField):
                    # Image/File fields: Prüfe ob neues Bild hochgeladen wurde
                    name_in_db = strip_name_of_underscores_begin_end(field_name)
                    
                    # Prüfe ob "clear" Checkbox aktiviert ist
                    clear_checkbox_name = f"{field_name}-clear"
                    should_clear = clear_checkbox_name in request.POST
                    
                    if should_clear:
                        # Bild löschen wenn Checkbox aktiviert
                        if hasattr(user, name_in_db):
                            old_file = getattr(user, name_in_db)
                            if old_file:
                                # Bestimme den Dateipfad (kann FileField-Objekt oder String sein)
                                file_path = old_file.name if hasattr(old_file, 'name') else str(old_file)
                                # Lösche alte Datei vom Server
                                if file_path and default_storage.exists(file_path):
                                    default_storage.delete(file_path)
                                # Lösche aus DB
                                setattr(user, name_in_db, None)
                    elif field_name in request.FILES:
                        # Neues Bild wurde hochgeladen
                        uploaded_file = request.FILES[field_name]
                        
                        # Lösche altes Bild falls vorhanden
                        if hasattr(user, name_in_db):
                            old_file = getattr(user, name_in_db)
                            if old_file:
                                # Bestimme den Dateipfad (kann FileField-Objekt oder String sein)
                                file_path = old_file.name if hasattr(old_file, 'name') else str(old_file)
                                if file_path and default_storage.exists(file_path):
                                    default_storage.delete(file_path)
                        
                        # Speichere neues Bild
                        file_path = name_for_picture(user)
                        saved_path = default_storage.save(file_path, uploaded_file)
                        
                        # Speichere in DB: Django's ImageField kann direkt mit dem Pfad arbeiten
                        if hasattr(user, name_in_db):
                            # Weise die gespeicherte Datei dem ImageField zu
                            # saved_path ist relativ zu MEDIA_ROOT
                            setattr(user, name_in_db, saved_path)
                    # Wenn kein neues Bild und keine Clear-Checkbox: behalte alten Wert
                    # (nichts tun)
                    
                else:
                    # non-checkbox, non-image fields
                    value = request.POST.get(field_name, '')
                    name_in_db = strip_name_of_underscores_begin_end(field_name)
                    if hasattr(user, name_in_db):
                        setattr(user, name_in_db, value)

            user.save()
            # messages.success(request, "Daten gespeichert!")
            return redirect("appPFE:docForm")
            
        elif action == 'send':
            # SEND: MIT Validierung (alle Pflichtfelder müssen ausgefüllt sein)
            form = WholeDocument(request.POST, request.FILES)
            
            if form.is_valid():
                document = form.save(commit=False)
                document.user = request.user
                document.save()

                # save image in media/images
            for field_name, field_value in request.FILES.items():
                        from django.core.files.storage import default_storage
                        
                        file_name = f"{request.user.id}_{field_name}.png"
                        file_path = os.path.join('images', file_name)
                        default_storage.save(file_path, field_value)

                        
                        field_name_without_underscored = strip_name_of_underscores_begin_end(field_name)
                        if hasattr(user, field_name_without_underscored):
                            setattr(user, field_name_without_underscored, saved_path)

            user.save()
            return redirect("appPFE:success")
    
    else:
        # GET: Form mit gespeicherten User-Daten vorausfüllen
        initial_data = {}
        if request.user.is_authenticated:
            for field_name in WholeDocument().fields.keys():
                # name_with_underscored = add_underscored_to_name_begin_end(field_name)
                name_in_db = strip_name_of_underscores_begin_end(field_name)

                if(name_in_db == "Photo_portrait"): 
                    print(name_in_db, "in loading from db")
                    if hasattr(request.user, name_in_db):
                        value = getattr(request.user, name_in_db)
                        print(value)
                        print(bool(value))

                if hasattr(request.user, name_in_db):
                    value = getattr(request.user, name_in_db)
                    if value:  # Nur wenn Wert vorhanden
                        initial_data[field_name] = value
        
        form = WholeDocument(initial=initial_data)
    
    # Checke ob neuer User
    is_new_user = request.session.pop('is_new_user', False)
    
    # Zähle ausgefüllte Felder
    number_filled_fields = 0
    number_total_fields = 0
    
    if request.user.is_authenticated:
        for field_name in WholeDocument().fields.keys():
            field_name_without_underscored = strip_name_of_underscores_begin_end(field_name)
            if hasattr(request.user, field_name_without_underscored):
                number_total_fields += 1
                value = getattr(request.user, field_name_without_underscored)
                # Check ob Feld ausgefüllt ist
                if value and value != '':
                    number_filled_fields += 1
    
    # Prozentsatz berechnen
    if number_total_fields > 0:
        completion_percentage = int((number_filled_fields / number_total_fields) * 100)
    else:
        completion_percentage = 0
    
    context = {
        'form': form,
        'translatable_fields': form.autotranslatable,
        'is_new_user': is_new_user,
        'number_filled_fields': number_filled_fields,
        'number_total_fields': number_total_fields,
        'completion_percentage': completion_percentage,  # ← NEU
    }

    return render(request, "appPFE/document_form.html", context)

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