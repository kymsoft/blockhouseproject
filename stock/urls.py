from django.urls import path
from . import views

app_name = 'stock'

urlpatterns = [
    path('', views.fetch_data_view),
    path('backtest/', views.backtest_view, name="backtest"),
    path('predictions/', views.view_predictions, name="predictions"),
    path('report/', views.generate_report, name="report"),
]
