# market_data/services/alpha_vantage_service.py
from .base_service import BaseAPIService

class AlphaVantageService(BaseAPIService):
    def get_stock_quote(self, symbol):
        """
        Get real-time stock quote
        """
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': symbol
        }
        return self._make_request(params)
    
    def get_company_overview(self, symbol):
        """
        Get company overview
        """
        params = {
            'function': 'OVERVIEW',
            'symbol': symbol
        }
        return self._make_request(params)

    def get_options_chain(self, symbol):
        """
        Get options chain data
        """
        params = {
            'function': 'OPTIONS',
            'symbol': symbol
        }
        return self._make_request(params)