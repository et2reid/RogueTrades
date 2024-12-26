# market_data/services/alpha_vantage_service.py
from datetime import datetime
from django.core.cache import cache
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

    def get_daily_prices(self, symbol):
        """
        Fetch daily price data for a given symbol.
        Returns cached data if available, otherwise fetches from API.
        """
        cache_key = f'alpha_vantage_daily_{symbol}'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
            
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': symbol,
            'outputsize': 'compact'  # Last 100 data points
        }
        
        raw_data = self._make_request(params)
        processed_data = self._process_daily_data(raw_data)
        
        # Cache the processed data
        cache.set(cache_key, processed_data, 900)  # Cache for 15 minutes
        
        return processed_data
            
    def _process_daily_data(self, raw_data):
        """Transform the raw API data into a more usable format."""
        time_series = raw_data.get('Time Series (Daily)', {})
        processed_data = []
        
        for date, values in time_series.items():
            processed_data.append({
                'date': datetime.strptime(date, '%Y-%m-%d').date(),
                'open': float(values['1. open']),
                'high': float(values['2. high']),
                'low': float(values['3. low']),
                'close': float(values['4. close']),
                'volume': int(values['5. volume'])
            })
        
        # Sort by date descending
        processed_data.sort(key=lambda x: x['date'], reverse=True)
        return processed_data

    def get_intraday_prices(self, symbol, interval='5min'):
        """
        Fetch intraday price data for a given symbol.
        Interval options: 1min, 5min, 15min, 30min, 60min
        """
        cache_key = f'alpha_vantage_intraday_{symbol}_{interval}'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
            
        params = {
            'function': 'TIME_SERIES_INTRADAY',
            'symbol': symbol,
            'interval': interval,
            'outputsize': 'compact'
        }
        
        raw_data = self._make_request(params)
        processed_data = self._process_intraday_data(raw_data, interval)
        
        cache.set(cache_key, processed_data, 300)  # Cache for 5 minutes
        
        return processed_data

    def _process_intraday_data(self, raw_data, interval):
        """Transform the raw intraday API data into a more usable format."""
        time_series_key = f'Time Series ({interval})'
        time_series = raw_data.get(time_series_key, {})
        processed_data = []
        
        for timestamp, values in time_series.items():
            processed_data.append({
                'timestamp': datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S'),
                'open': float(values['1. open']),
                'high': float(values['2. high']),
                'low': float(values['3. low']),
                'close': float(values['4. close']),
                'volume': int(values['5. volume'])
            })
        
        # Sort by timestamp descending
        processed_data.sort(key=lambda x: x['timestamp'], reverse=True)
        return processed_data