from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
#from .models import CustomUser 

User = get_user_model()

def register(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

    if form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'usuário registrado com sucesso')
        return redirect('index')     
           
    else:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f'algo deu errado no campo {field} : {error}')

    return render(request, 'register.html', {'form' : form})

#def valid_user(form):
     
    
def user_login(request):
    if request.method == "POST":
        if "logout" in request.POST:
            logout(request)
            return HttpResponse("Usuário deslogado com sucesso")
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse ('usuario logado') 
        else:
            return render(request, 'login.html', {'error': 'Usuário ou senha inválidos.'})

    return render(request, 'login.html')

@login_required
def follow_unfollow(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    
    if request.user != target_user:
        if target_user in request.user.following.all():
            request.user.following.remove(target_user)  # Deixar de seguir
        else:
            request.user.following.add(target_user)  # Seguir

    return redirect('tela_usuario_other', user_id=user_id)

