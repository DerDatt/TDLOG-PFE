from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import generic
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from accounts.forms import LoginOrRegisterForm
from .models import WholeDocument
from accounts.models import MyUser
from auto_translation.Traducteur import traduire_fr_en
from django.contrib.auth.decorators import login_required

from . import utils


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


class IndexView(generic.ListView):
    template_name = "appPFE/index.html"
    # context_object_name = "latest_question_list"

    def get(self, request, *args, **kwargs):
        """Redirect to document form"""
        return redirect('appPFE:docForm')

    def get_queryset(self):
        """Return the last five published questions."""
        return HttpResponse("dsdsasadsasdasadsadsad ")


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
    
    if stats['filled_fields'] == stats['total_fields']:
        request.user.form_complete = True
    else:
        request.user.form_complete = False

    request.user.save()

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


def success_view(request):
    return render(request, "appPFE/success.html")
