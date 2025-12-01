from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.views import generic
# from .forms import ContactForm, DocumentForm
from .models import WholeDocument


def index(request):
    return HttpResponse("This here is the index of our () PFE (Projet final etudes or similar lol). ")

class IndexView(generic.ListView):
    template_name = "appPFE/index.html"
    context_object_name = "latest_question_list"

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

def doc_view(request):
    # path = "appPFE/field_data.csv"
    if request.method == "POST":
        form = WholeDocument(request.POST) #, path_csv = path)
        if form.is_valid():
            form.save()
            # redirect to function to generated LaTeX and give download button

            return redirect("appPFE:success")
        else: 
            print("Not Valid")
    else:
        form = WholeDocument()# path_csv = path)

    return render(request, "appPFE/document_form.html", {"form": form})



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