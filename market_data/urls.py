# market_data/urls.py
from django.urls import path
from .views import HomeView, StockDetailView  # Removed intraday_data

app_name = 'market_data'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('stock/<str:symbol>/', StockDetailView.as_view(), name='stock_detail'),
]