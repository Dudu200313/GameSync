from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .services import IGDBAPI
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from .models import Playlist, Wishlist, Owned, Logview
from .services_itad import ITADAPI
from .forms import LogviewForm, CustomUser
from django.core.cache import cache
from django.db.models import Q

def index(request):
    igdb = IGDBAPI()
    popular_games = igdb.fetch_most_popular_games()

    latest_activities = []

    if request.user.is_authenticated:
        # Obtém os IDs dos amigos
        friends = request.user.following.all()
        
        # Obtém os últimos 6 registros de Logview dos amigos
        latest_activities = Logview.objects.filter(user__in=friends).order_by('-logview_date')[:6]

        # Obtém as capas dos jogos
        for activity in latest_activities:
            game = igdb.fetch_game_by_id(activity.game_id)
            activity.cover_url = game['cover']['url'].replace('t_thumb', 't_cover_big') if 'cover' in game else None

    context = {
        'popular_games': popular_games if popular_games else [],
        'latest_activities': latest_activities
    }
    return render(request, 'index.html', context)

def search_results(request):
    query = request.GET.get('q', '')

    if query:
        igdb = IGDBAPI()
        games = igdb.search_games(query)
    else:
        games = []

    return render(request, 'search_results.html', {'query': query, 'games': games})

def game_detail(request, game_id):
    igdb = IGDBAPI()
    itad = ITADAPI()

    # Default country (if not selected yet)
    selected_country = request.session.get('selected_country', 'br')

    if request.method == 'POST' and 'select_country' in request.POST:
        selected_country = request.POST['select_country']
        request.session['selected_country'] = selected_country

    game = igdb.fetch_game_by_id(game_id)
    itad_price = itad.pick_price(game['name'],selected_country)
    logviews = Logview.objects.filter(game_id=game_id)
    form = LogviewForm()
    
    if request.method == 'POST':
        form = LogviewForm(request.POST)
        if form.is_valid():
            logview = form.save(commit=False)
            logview.user = request.user
            logview.game_id = game_id
            logview.save()
            game_name = game.get('name')
            add_to_playlist(request, game_id, game_name)
            return redirect('game_detail', game_id=game_id)

    if game:
        genres = [genre['name'] for genre in game.get('genres', [])]
        platforms = [platform['name'] for platform in game.get('platforms', [])]
        developers = [company['company']['name'] for company in game.get('involved_companies', []) if company.get('developer')]

        context = {
            'game_id': game.get('id'),
            'name': game.get('name'),
            'summary': game.get('summary', 'História não disponível.'),
            'developers': developers[0] if developers else 'Desenvolvedor desconhecido',
            'first_release_date': game.get('first_release_date', 'Ano de lançamento desconhecido'),
            'cover_url': game['cover']['url'].replace('t_thumb', 't_cover_big') if 'cover' in game else None,
            'related_games': igdb.fetch_games_by_series(game.get('collections'), game_id) if game.get('collections') else [],
            'similar_games': game.get('similar_games', []),
            'genres': genres,
            'platforms': platforms,
            'itad_price' : itad_price,
            'selected_country' : selected_country,
            'logviews': logviews,
            'form': form,
        }
        return render(request, 'game_detail.html', context)
    else:
        return render(request, '404.html', status=404)

@login_required
def add_to_playlist(request, game_id, game_name):
    user = request.user
    igdb = IGDBAPI()
    game = igdb.fetch_game_by_id(game_id)

    # Verifica se o jogo já está na playlist
    if Playlist.objects.filter(user=user, game_id=game_id).exists():
        messages.info(request, "Este jogo já está na sua playlist!")
    else:
        cover_url = game['cover']['url'].replace('t_thumb', 't_cover_big') if 'cover' in game else None

        Playlist.objects.create(user=user, game_id=game_id, game_name=game_name, cover_url=cover_url)
        messages.success(request, "Jogo adicionado à sua playlist!")

    return redirect('game_detail', game_id=game_id)  # Redireciona para a página do jogo

@login_required
def add_to_wishlist(request, game_id, game_name):
    user = request.user
    igdb = IGDBAPI()
    game = igdb.fetch_game_by_id(game_id)

    # Verifica se o jogo já está na wishlist
    if Wishlist.objects.filter(user=user, game_id=game_id).exists():
        messages.info(request, "Este jogo já está na sua wishlist!")
    else:
        cover_url = game['cover']['url'].replace('t_thumb', 't_cover_big') if 'cover' in game else None

        Wishlist.objects.create(user=user, game_id=game_id, game_name=game_name, cover_url=cover_url)
        messages.success(request, "Jogo adicionado à sua wishlist!")

    return redirect('game_detail', game_id=game_id)  # Redireciona para a página do jogo

@login_required
def add_to_owned(request, game_id, game_name):
    user = request.user
    igdb = IGDBAPI()
    game = igdb.fetch_game_by_id(game_id)

    # Verifica se o jogo já está na owned
    if Owned.objects.filter(user=user, game_id=game_id).exists():
        messages.info(request, "Este jogo já está na sua owned!")
    else:
        cover_url = game['cover']['url'].replace('t_thumb', 't_cover_big') if 'cover' in game else None

        Owned.objects.create(user=user, game_id=game_id, game_name=game_name, cover_url=cover_url)
        messages.success(request, "Jogo adicionado à sua owned!")

    return redirect('game_detail', game_id=game_id)  # Redireciona para a página do jogo

@login_required
def user_playlist(request):
    playlist = Playlist.objects.filter(user=request.user)
    return render(request, 'playlist.html', {'playlist': playlist})

@login_required
def user_wishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist': wishlist})

@login_required
def user_owned(request):
    owned = Owned.objects.filter(user=request.user)
    return render(request, 'owned.html', {'owned': owned})

@login_required
def user_diary(request):
    diary = Playlist.objects.filter(user=request.user)
    return render(request, 'diary.html', {'diary': diary})


def other(request):
    return HttpResponse("other pageeee by ianzera")

@login_required
def tela_usuario(request, user_id=None):
    if user_id:
        user = get_object_or_404(CustomUser, id=user_id)
    else:
        user = request.user 

    return render(request, 'tela_usuario.html', {'user': user})
