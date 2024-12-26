# market_data/views.py
from django.views.generic import TemplateView
from .services.alpha_vantage_service import AlphaVantageService
import logging

logger = logging.getLogger(__name__)

class HomeView(TemplateView):
    template_name = 'market_data/home.html'

class StockDetailView(TemplateView):
    template_name = 'market_data/stock_detail.html'  # Back to your original template
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        symbol = kwargs.get('symbol', '').upper()
        
        try:
            service = AlphaVantageService()
            
            # Get stock data
            quote = service.get_stock_quote(symbol)
            daily_data = service.get_daily_prices(symbol)
            company_info = service.get_company_overview(symbol)
            
            # Process quote data for display
            latest_price = None
            if quote and 'Global Quote' in quote:
                latest_price = {
                    'price': float(quote['Global Quote']['05. price']),
                    'change': float(quote['Global Quote']['09. change']),
                    'change_percent': float(quote['Global Quote']['10. change percent'].rstrip('%')),
                    'volume': int(quote['Global Quote']['06. volume'])
                }
            
            context.update({
                'symbol': symbol,
                'company_info': company_info,
                'latest_price': latest_price,
                'daily_data': daily_data,
                'error': None
            })
            
            logger.info(f"Successfully fetched data for {symbol}")
            
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {str(e)}")
            context.update({
                'symbol': symbol,
                'error': "Unable to fetch market data at this time. Please try again later."
            })
        
        return context