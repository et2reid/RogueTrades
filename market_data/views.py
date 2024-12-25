from django.shortcuts import render

# Create your views here.
# market_data/views.py
from django.shortcuts import render
from django.views.generic import TemplateView
from .services.alpha_vantage_service import AlphaVantageService

class HomeView(TemplateView):
    template_name = 'market_data/home.html'

class StockDetailView(TemplateView):
    template_name = 'market_data/stock_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        symbol = self.kwargs.get('symbol')
        
        service = AlphaVantageService()
        
        # Fetch data from Alpha Vantage
        quote_data = service.get_stock_quote(symbol)
        company_data = service.get_company_overview(symbol)
        options_data = service.get_options_chain(symbol)
        
        context.update({
            'symbol': symbol,
            'quote_data': quote_data,
            'company_data': company_data,
            'options_data': options_data,
        })
        
        return context