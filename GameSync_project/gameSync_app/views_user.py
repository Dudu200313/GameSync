from django.shortcuts import render
from django.http import HttpResponse
from .forms import CustomUserCreationForm

def register(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
    
    if form.is_valid():
        form.save()
        return HttpResponse('User registerd succesfully')            
    
    return render(request, 'register.html', {'form' : form})
    