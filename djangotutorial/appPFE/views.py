import os
from django import forms
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import generic
from django.views.generic import RedirectView
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse_lazy
# from .forms import ContactForm, DocumentForm
from accounts.forms import LoginOrRegisterForm
from .models import WholeDocument  # , LoginForm
from accounts.models import MyUser
from auto_translation.Traducteur import traduire_fr_en, traduire_fr_en_dummy
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage

from . import utils


def login_or_register_view(request):
    """Login or Register - if user exists: Login, otherwise: Register"""
    if request.user.is_authenticated:
        logout(request)
        
    if request.method == "POST":
        form = LoginOrRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # user exists and password is correct
                login(request, user)
                return redirect('appPFE:docForm')
            else:
                # user does not exist or wrong password
                try:
                    MyUser.objects.get(username=username)
                    # user exists → wrong password
                    messages.error(request, "Wrong password")
                except MyUser.DoesNotExist:
                    # user does not exist → create new user
                    user = MyUser.objects.create_user(
                        username=username,
                        password=password
                    )
                    login(request, user)

                    # mark user as new
                    request.session['is_new_user'] = True

                    return redirect('appPFE:docForm')
    else:
        form = LoginOrRegisterForm()

    return render(request, "appPFE/login_or_register.html", {"form": form})


def login_view(request):
    """Login - gives error if user doesn't exust. """
    if request.user.is_authenticated:
        logout(request)
        
    if request.method == "POST":
        form = LoginOrRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # user exists and password is correct
                login(request, user)
                return redirect('appPFE:docForm')
            else:
                # user does not exist or wrong password
                try:
                    MyUser.objects.get(username=username)
                    # user exists → wrong password
                    messages.error(request, "Wrong password")
                except MyUser.DoesNotExist:
                    # user does not exist → create new user
                    messages.error(request, "User does not exist. To create a new user, please contact an admin. ")

                    return redirect('appPFE:docForm')
    else:
        form = LoginOrRegisterForm()

    return render(request, "appPFE/login.html", {"form": form})


def logout_view(request):
    """Logout and redirect to login page"""
    logout(request)
    return redirect('appPFE:login')


def index(request):
    return HttpResponse("This here is the index of our () PFE (Projet final etudes or similar lol). ")


class IndexView(generic.ListView):
    template_name = "appPFE/index.html"
    # context_object_name = "latest_question_list"

    def get(self, request, *args, **kwargs):
        """Redirect to document form"""
        return redirect('appPFE:docForm')

    def get_queryset(self):
        """Return the last five published questions."""
        return HttpResponse("dsdsasadsasdasadsadsad ")

# class DocView(generic.FormView): 
#     template_name = "appPFE/document_form.html"
#     form_class = DocumentForm
#     success_url = "/success/"

#     def form_valid(self, form):
#         # here you can save, send mail, log, etc.
#         print(form.cleaned_data)
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = "Fill out document"
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


@login_required
def doc_view(request):
    if request.method == "POST":
        action = request.POST.get('action')
        
        if action == 'save':
            # SAVE: without validation
            utils.save_form_data_to_user(
                request.user,
                WholeDocument,
                request.POST,
                request.FILES,
                validate=False
            )
            return redirect("appPFE:docForm")
        
        elif action == 'send':
            # SEND: with validation
            validated_form = utils.save_form_data_to_user(
                request.user, 
                WholeDocument, 
                request.POST, 
                request.FILES, 
                validate=True
            )
            
            # validated_form is None if validate=False, or a form object if validate=True
            # If form exists but is not valid, show errors
            if validated_form is not None and not validated_form.is_valid():
                # Validation failed
                return render(request, "appPFE/document_form.html", {
                    "form": validated_form,
                    "translatable_fields": validated_form.autotranslatable,
                })

            # Form is valid - validated_form has cleaned_data because is_valid() was called
            validated_form.send(request.user)
            
            # Success
            return redirect("appPFE:success")
    
    # GET: Pre-fill form with saved user data
    form = utils.load_user_data_into_form(request.user, WholeDocument)
    
    # Check if new user
    is_new_user = request.session.pop('is_new_user', False)
    
    # Calculate completion stats
    stats = utils.calculate_completion_stats(request.user, WholeDocument)
    
    context = {
        'form': form,
        'translatable_fields': form.autotranslatable,
        'is_new_user': is_new_user,
        'number_filled_fields': stats['filled_fields'],
        'number_total_fields': stats['total_fields'],
        'completion_percentage': stats['completion_percentage'],
    }
    
    # set form_complete in user: 
    print("stats['filled_fields']", stats['filled_fields'])
    print("stats['total_fields']", stats['total_fields'])
    if stats['filled_fields'] == stats['total_fields']:
        request.user.form_complete = True
    else:
        request.user.form_complete = False

    request.user.save()

    return render(request, "appPFE/document_form.html", context)


# @login_required
# def doc_view(request):
#     if request.method == "POST":
#         # Check which button was clicked
#         action = request.POST.get('action')
        
#         if action == 'save':
#             # SAVE: Save WITHOUT validation (even with empty fields)
#             user = request.user
#             tmp_form = WholeDocument()
#             # print("=== DEBUG SAVE ===")
#             # print("Form-Felder:", WholeDocument().fields.keys())
#             # print("POST-Daten:", request.POST.keys())
#             # print("User-Attribute:", [field.name for field in user._meta.get_fields()])


#             # Read directly from POST data (without form validation)
#             for field_name, field in tmp_form.fields.items():

#                 if isinstance(field, forms.BooleanField):
#                     # Checkbox: True if in POST, else False
#                     value = field_name in request.POST
#                     name_in_db = get_db_field_name(field_name)
#                     if hasattr(user, name_in_db):
#                         setattr(user, name_in_db, value)
                        
#                 elif isinstance(field, forms.ImageField):
#                     # Image/File fields: Check if new image was uploaded
#                     name_in_db = get_db_field_name(field_name)
                    
#                     # Check if "clear" checkbox is activated
#                     clear_checkbox_name = f"{field_name}-clear"
#                     should_clear = clear_checkbox_name in request.POST
                    
#                     if should_clear:
#                         # Delete image if checkbox is activated
#                         if hasattr(user, name_in_db):
#                             old_file = getattr(user, name_in_db)
#                             if old_file:
#                                 # Determine the file path (can be FileField object or string)
#                                 file_path = old_file.name if hasattr(old_file, 'name') else str(old_file)
#                                 # Delete old file from server
#                                 if file_path and default_storage.exists(file_path):
#                                     default_storage.delete(file_path)
#                                 # Delete from DB
#                                 setattr(user, name_in_db, None)
#                     elif field_name in request.FILES:
#                         # New image was uploaded
#                         uploaded_file = request.FILES[field_name]
                        
#                         # Delete old image if present
#                         if hasattr(user, name_in_db):
#                             old_file = getattr(user, name_in_db)
#                             if old_file:
#                                 # Determine the file path (can be FileField object or string)
#                                 file_path = old_file.name if hasattr(old_file, 'name') else str(old_file)
#                                 if file_path and default_storage.exists(file_path):
#                                     default_storage.delete(file_path)
                        
#                         # Save new image
#                         file_path = name_for_picture(user)
#                         saved_path = default_storage.save(file_path, uploaded_file)
                        
#                         # Save to DB: Django's ImageField can work directly with the path
#                         if hasattr(user, name_in_db):
#                             # Assign the saved file to the ImageField
#                             # saved_path is relative to MEDIA_ROOT
#                             setattr(user, name_in_db, saved_path)
#                     # If no new image and no clear checkbox: keep old value
#                     # (do nothing)
                    
#                 else:
#                     # non-checkbox, non-image fields
#                     value = request.POST.get(field_name, '')
#                     name_in_db = get_db_field_name(field_name)
#                     if hasattr(user, name_in_db):
#                         setattr(user, name_in_db, value)

#             user.save()
#             # messages.success(request, "Data saved!")
#             return redirect("appPFE:docForm")
            
#         elif action == 'send':
#             # SEND: WITH validation (all required fields must be filled)
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
#         # GET: Pre-fill form with saved user data
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
#                     if value:  # Only if value exists
#                         initial_data[field_name] = value
        
#         form = WholeDocument(initial=initial_data)
    
#     # Check if new user
#     is_new_user = request.session.pop('is_new_user', False)
    
#     # Count filled fields
#     number_filled_fields = 0
#     number_total_fields = 0
    
#     if request.user.is_authenticated:
#         for field_name in WholeDocument().fields.keys():
#             field_name_without_underscored = get_db_field_name(field_name)
#             if hasattr(request.user, field_name_without_underscored):
#                 number_total_fields += 1
#                 value = getattr(request.user, field_name_without_underscored)
#                 # Check if field is filled
#                 if value and value != '':
#                     number_filled_fields += 1
    
#     # Calculate percentage
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
