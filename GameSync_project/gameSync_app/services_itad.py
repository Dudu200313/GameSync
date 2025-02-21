import requests
from django.conf import settings


class ITADAPI:
    def __init__(self):
        self.baseUrl = settings.ITAD_BASE_URL   
        self.apiKey = settings.ITAD_ACCESS_TOKEN
        self.clientId = settings.ITAD_CLIENT_ID
        self.clientSecret = settings.ITAD_CLIENT_SECRET     

    def get_game_id(self,game_name):
        url = f'{self.baseUrl}/lookup/id/title/v1?key={self.apiKey}'

        json_payload = [game_name]

        if not json_payload:
            return {
                'error': 'No game IDs found',
                'status_code': 404,
                'details': f'No matching game ID for "{game_name}"'
            }

        response = requests.post(
            url = url,
            params={'key' : self.apiKey},
            json = json_payload,
            headers={'Content-Type': 'application/json'} 
        )

        if response.status_code == 200:
            response_data = response.json()
            # Get the game ID for the requested game
            game_id = response_data.get(game_name)

            if game_id:
                return [game_id]  # Return the ID as an array (required format)
            else:
                return []  # Return an empty array if the game is not found
        else:
            return {
                'error': 'Failed to fetch game IDs',
                'status_code': response.status_code,
                'details': response.text
            }
        
   # def beautify_shop(shoped):

         

    def pick_price(self,game_name):
        url = f'{self.baseUrl}/games/prices/v3?key={self.apiKey}'

        json_payload = self.get_game_id(game_name)
        
        response = requests.post(
            url = url,
            params={'key' : self.apiKey,
                    'country' : 'br',
                    'deals' : 'true',      
            },
            json = json_payload,
            headers={'Content-Type': 'application/json'} 
        )  

        if response.status_code == 200:
            get_response = response.json()
            
            filtering_deals = []
            for i in get_response:
                filtering_deals.append(i['deals'])

            filtering_shops = []
            for i in filtering_deals:
                for j in i:
                    filtering_shops.append(j['shop'])
                    filtering_shops.append(j['price'])
            return filtering_shops
            
        else:
            return {
                'error': 'Failed to fetch prices',
                'status_code': response.status_code,
                'details': response.text
            }      

