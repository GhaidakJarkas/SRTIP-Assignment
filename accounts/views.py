from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from accounts.models import CustomUser
from accounts.forms import CustomUserCreationForm


def user_login(request):
    if request.user.is_authenticated:
        return redirect('core:index')
    else:

        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            print(email, password)
            user = authenticate(request, email=email, password=password)
            print(user)
            if user is not None:
                login(request, user)
                return redirect('core:index')
            else:
                messages.error(request, "Email or Password is incorrect", extra_tags="danger")
                return redirect('core:login')
        return render(request, "core/login.html")
    

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('core:login')


def users(request):
    users = CustomUser.objects.all()
    ctx = {
        "users": users
    }

    return render(request, "core/users.html", ctx)

def create_user(request):
    if request.method == 'POST':
        data = request.POST.copy()
        print(data)
        form = CustomUserCreationForm(data)
        
        if form.is_valid():
            print('VALID')
            form.save()
        print('not valid')
        print(form.errors)
    return render(request, "core/create-user.html")
