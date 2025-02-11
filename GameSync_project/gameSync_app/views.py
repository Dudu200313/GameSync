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

def game_detail(request, game_id):
    igdb = IGDBAPI()
    game = igdb.fetch_game_by_id(game_id)

    if game:
        genres = [genre['name'] for genre in game.get('genres', [])]
        platforms = [platform['name'] for platform in game.get('platforms', [])]
        developers = [company['company']['name'] for company in game.get('involved_companies', []) if company.get('developer')]

        context = {
            'name': game.get('name'),
            'storyline': game.get('storyline', 'História não disponível.'),
            'developers': developers[0],
            'first_release_date': game.get('first_release_date', [{'date': 'Data desconhecida'}]),
            'cover_url': game['cover']['url'].replace('t_thumb', 't_cover_big') if 'cover' in game else None,
            'related_games': igdb.fetch_games_by_series(game.get('collections')) if game.get('collections') else [],
            'similar_games': game.get('similar_games', []),
            'genres': genres,
            'platforms': platforms,
        }
        return render(request, 'game_detail.html', context)
    else:
        return render(request, '404.html', status=404)

def other(request):
    return HttpResponse("other pageeee by ianzera")
# Create your views here.
