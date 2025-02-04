import requests
from django.conf import settings

class IGDBAPI:
    def __init__(self):
        self.base_url = settings.IGDB_BASE_URL
        self.headers = {
            'Client-ID': settings.IGDB_CLIENT_ID,
            'Authorization': f'Bearer {settings.IGDB_ACCESS_TOKEN}',
        }
    
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
                return response.json()
            else:
                print(f"Error fetching game details: {response.status_code} - {response.text}")
                return None
        else:
            print(f"Error fetching popular games: {response.status_code} - {response.text}")
            return None