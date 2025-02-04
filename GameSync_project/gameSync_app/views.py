from django.shortcuts import render
from django.http import HttpResponse
from .services import IGDBAPI

def index(request):
    igdb = IGDBAPI()
    popular_games = igdb.fetch_most_popular_games()

    context = {
        'popular_games': popular_games if popular_games else []
    }
    return render(request, 'index.html', context)

def other(request):
    return HttpResponse("other pageeee by ianzera")
# Create your views here.
