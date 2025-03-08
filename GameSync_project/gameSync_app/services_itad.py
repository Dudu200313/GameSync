import requests
from django.conf import settings

class ITADAPI:
    def __init__(self):
        self.baseUrl = settings.ITAD_BASE_URL
        self.apiKey = settings.ITAD_ACCESS_TOKEN

    def get_game_id(self,game_name):
        url = f'{self.baseUrl}/lookup/id/title/v1'
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
            game_id = response.json().get(game_name)
            return [game_id] if game_id else []
        else:
            return {
                'error': 'Failed to fetch game IDs',
                'status_code': response.status_code,
                'details': response.text
            }
        
   # def beautify_shop(shoped):

    def pick_price(self,game_name,country):
        url = f'{self.baseUrl}/games/prices/v3'
        params={'key' : self.apiKey,
                'country' : country,
                'deals' : 'true'
        }

        json_payload = self.get_game_id(game_name)
        response = requests.post(
            url = url,
            params=params,
            json = json_payload,
            headers={'Content-Type': 'application/json'}
        )  

        if response.status_code == 200:
            get_response = response.json()
            all_deals = []

            for i in get_response:
                all_deals.extend(i['deals'])

            if not all_deals:
                params['deals'] = 'false'
                response = requests.post(
                    url = url,
                    params=params,
                    json = json_payload,
                    headers={'Content-Type': 'application/json'}
                )

                if response.status_code == 200:
                    get_response = response.json()
                    all_deals = []

                    for i in get_response:
                        all_deals.extend(i['deals'])
            
            min_price = None
            best_shop = None
            
            for deal in all_deals:
                price = deal['price']['amount']
                if min_price is None or price < min_price:
                    min_price = price
                    best_shop = deal['shop']['name']

            if min_price is not None:
                return {
                    'shop_name': best_shop,
                    'price': min_price,
                }
            
        else:
            return {
                'error': 'Failed to fetch prices',
                'status_code': response.status_code,
                'details': response.text
            }
