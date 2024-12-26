# market_data/services/base_service.py
import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

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
            
            data = response.json()
            
            # Check for API error messages
            if 'Error Message' in data:
                logger.error(f"Alpha Vantage API Error: {data['Error Message']}")
                return None
                
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API Request Error: {str(e)}")
            return None
        except ValueError as e:
            logger.error(f"JSON Parsing Error: {str(e)}")
            return None