from django.shortcuts import render, redirect
from django.contrib.auth.forms import (
    AuthenticationForm, 
    PasswordChangeForm,
    UserChangeForm
)
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.contrib import messages
from .forms import NewUserForm, EditProfileForm
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.http import HttpResponse


# Create your views here.
def homepage(request):
    return render(request = request,
                  template_name='main/home.html',
                  context = {})

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Akun baru dibuat: {username}")
            login(request, user)
            messages.info(request,f"Anda masuk sebagai: {username}")
            return redirect("main:homepage")

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(request = request,
                          template_name = "main/register.html",
                          context={"form":form})

    form = NewUserForm
    return render(request = request,
                  template_name = "main/register.html",
                  context={"form":form})

def logout_request(request):
    logout(request)
    # messages.info(request, "Berhasil Keluar Akun!")
    return redirect("main:login")

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # messages.info(request,f"Anda masuk sebagai: {username}")
                return redirect("main:homepage")
            else:
                messages.error(request, "Username atau Kata Sandi Tidak Sesuai")
        else:
            messages.error(request, "Username atau Kata Sandi Tidak Sesuai")
    form = AuthenticationForm()
    return render(request, 
                    "main/login.html", 
                    {"form":form})

def profile(request):
    args = {"user": request.user}
    return render(request, "main/profile.html", args)

def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect("main:profile")
    else:
        form = EditProfileForm(instance=request.user)
        args = {"form": form}
        return render(request,"main/edit_profile.html",args)

def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect("main:profile")
        else:
            return redirect("main:change_password")
    else:
        form = PasswordChangeForm(user=request.user)
        args = {"form": form}
        return render(request,"main/change_password.html",args)