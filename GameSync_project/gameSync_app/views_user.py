from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm

def register(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
    
    if form.is_valid():
        form.save()
        return HttpResponse('User registerd succesfully')            
    
    return render(request, 'register.html', {'form' : form})
    
def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse ('usuario logado') 
        else:
            return render(request, 'login.html', {'error': 'Usuário ou senha inválidos.'})

    return render(request, 'login.html')