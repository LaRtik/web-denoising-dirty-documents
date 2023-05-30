from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout as lgout
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Documents
from .forms import DocumentForm, UserRegistrationForm
from .utils import clear_image

# Create your views here.


def index(request):
    return redirect("login")


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return HttpResponseRedirect(reverse("upload"))
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = UserRegistrationForm()
    context = {
        'form': form,
        'type': "Register",
    }
    return render(request, "register.html", context)


class LoginUser(LoginView):
    form = AuthenticationForm
    template_name = 'register.html'
    next_page = "upload"
    redirect_authenticated_user = True
    extra_context = {
        'type': "Login",
    }

@login_required(login_url="/login")
def result(request, document_id):
    document = Documents.objects.get(id=document_id)
    context = {
        'image_old': document.image.url,
        'image_new': document.result_image.url[6:],
        'text': document.image_text,
    }
    return render(request, "result.html", context)
    return HttpResponse(f"Image result page {document_id}")
    

@login_required(login_url="/login")
def upload(request):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = User.objects.get(username = request.user)
            instance.save()
            instance.result_image, instance.image_text = clear_image(instance.image.url)
            instance.save()
            return HttpResponseRedirect(reverse(f"result", args=[instance.id]))
    else:
        form = DocumentForm()
        context = {
            'form': form,
        }
        return render(request, "upload.html", context)

@login_required(login_url="/login")
def logout(request):
    lgout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect("login")

@login_required(login_url="/login")
def profile(request):
    documents = Documents.objects.all().filter(author=request.user)
    context = {
        'documents': documents,
    }
    return render(request, "profile.html", context)
