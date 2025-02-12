import requests
from django.conf import settings
from datetime import datetime, timezone

class IGDBAPI:
    def __init__(self):
        self.base_url = settings.IGDB_BASE_URL
        self.headers = {
            'Client-ID': settings.IGDB_CLIENT_ID,
            'Authorization': f'Bearer {settings.IGDB_ACCESS_TOKEN}',
        }
    
    def fetch_game_by_id(self, game_id):
        url = f'{self.base_url}games'
        query = f'''
            fields 
                name, 
                storyline, 
                first_release_date, 
                cover.url, 
                collections, 
                genres.name, 
                platforms.name, 
                similar_games.name, 
                similar_games.cover.url, 
                involved_companies.company.name, 
                involved_companies.developer;
            where id = {game_id};
        '''
        response = requests.post(url, headers=self.headers, data=query)

        if response.status_code == 200:
            game_data = response.json()
            if game_data:
                game = game_data[0]

                game['first_release_date'] = datetime.fromtimestamp(game['first_release_date'], timezone.utc).strftime('%d/%m/%y')

                # Buscar detalhes dos jogos similares, se houver
                if 'similar_games' in game and game['similar_games']:
                    similar_game_ids = [str(similar_game['id']) for similar_game in game['similar_games'] if isinstance(similar_game, dict) and 'id' in similar_game]

                    if similar_game_ids:  # Só faz a query se houver IDs válidos
                        similar_games_query = f'fields name, cover.url; where id = ({",".join(similar_game_ids)});'
                        similar_games_response = requests.post(url, headers=self.headers, data=similar_games_query)

                        if similar_games_response.status_code == 200:
                            game['similar_games'] = similar_games_response.json()
                        else:
                            game['similar_games'] = []
                    else:
                        game['similar_games'] = []

                return game
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    
    def fetch_most_popular_games(self, limit=10):
        url = f'{self.base_url}popularity_primitives'
        query = f'fields game_id,value,popularity_type; sort value desc; limit {limit}; where popularity_type = 3;'
        response = requests.post(url, headers=self.headers, data=query)

        if response.status_code == 200:
            data = response.json()
            game_ids = [str(game["game_id"]) for game in data]  # Coletar IDs dos jogos populares
            
            # Agora, buscar os detalhes dos jogos populares com os IDs obtidos
            game_details_query = f'fields name, cover.url; where id = ({",".join(game_ids)});'
            response = requests.post(f'{self.base_url}games', headers=self.headers, data=game_details_query)

            if response.status_code == 200:
                games = response.json()

                # Corrigindo a URL da imagem para uma qualidade melhor
                for game in games:
                    if "cover" in game:
                        game["cover"]["url"] = game["cover"]["url"].replace("t_thumb", "t_cover_big")  # ou outro tamanho

                return games
            else:
                print(f"Error fetching game details: {response.status_code} - {response.text}")
                return None
        else:
            print(f"Error fetching popular games: {response.status_code} - {response.text}")
            return None
    
    def fetch_games_by_series(self, series_id):
            url = f'{self.base_url}games'
            query = f'fields name, cover.url; where collections = {series_id};'
            response = requests.post(url, headers=self.headers, data=query)

            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error fetching games by series: {response.status_code} - {response.text}")
                return None