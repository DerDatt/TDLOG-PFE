from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import generic
# from .forms import ContactForm, DocumentForm
from .models import WholeDocument #, LoginForm
from auto_translation.Traducteur import traduire_fr_en, traduire_fr_en_dummy
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.decorators import login_required


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


@login_required
def doc_view(request):
    # path = "appPFE/field_data.csv"    

    if request.method == "POST":
        form = WholeDocument(request.POST, request.FILES) #, path_csv = path)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.save()
            # redirect to function to generated LaTeX and give download button

            # save image in media/images
            for field_name, field_value in form.cleaned_data.items():
                if isinstance(field_value, InMemoryUploadedFile):  # Das ist ein Bild
                    # Speichere die Datei
                    import os
                    from django.core.files.storage import default_storage
                    
                    file_path = os.path.join('images', 'picture.png')
                    # in future: make picture name name of student, or somehow id in db
                    default_storage.save(file_path, field_value)

                    # path = default_storage.save(file_path, field_value)
                    # Speichere 'path' in deiner Datenbank


            return redirect("appPFE:success")
        else: 
            print("Not Valid")
    else:
        form = WholeDocument()# path_csv = path)
    
    context = {
        'form': form,
        'translatable_fields': form.autotranslatable
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