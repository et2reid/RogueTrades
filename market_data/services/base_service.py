# market_data/services/base_service.py
import requests
from django.conf import settings

class BaseAPIService:
    def __init__(self):
        self.api_key = settings.ALPHA_VANTAGE_API_KEY
        self.base_url = "https://www.alphavantage.co/query"

    def _make_request(self, params):
        """
        Make a request to the Alpha Vantage API
        """
        try:
            params['apikey'] = self.api_key
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            # In a real application, you'd want to log this error
            print(f"API Request Error: {e}")
            return None