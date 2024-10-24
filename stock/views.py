from decimal import Decimal
from .models import StockData, Prediction, BacktestResult
from django.http import JsonResponse, HttpResponse
import requests
from django.views.decorators.csrf import csrf_exempt
from .forms import BacktestForm
from . import backtest
from . import report
import os
import joblib
import pandas as pd 
import kagglehub
from django.shortcuts import get_object_or_404
# Create your views here.

ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
KAGGLE_USERNAME=os.getenv('KAGGLE_USERNAME')
KAGGLE_KEY=os.getenv('KAGGLE_KEY')

@csrf_exempt
def fetch_data_view(request):
    if request.method == 'POST':
        symbol = request.POST['symbol']
        # URL for Alpha Vantage API call
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey={ALPHA_VANTAGE_API_KEY}'
        response = requests.get(url)
        data = response.json()

        if data:
            for date, values in data["Time Series (5min)"].items():
                try:
                    StockData.objects.create(
                        symbol=symbol,
                        date=date,
                        open_price=Decimal(values['1. open']),
                        high_price=Decimal(values['2. high']),
                        low_price=Decimal(values['3. low']),
                        close_price=Decimal(values['4. close']),
                        volume=int(values['5. volume']) 
                    )
                    return JsonResponse("Stored data stored successfully", safe=False)
                except:
                    return JsonResponse("Something went wrong", safe=False)

        else:
            raise Exception("API request limit reached or invalid request") 

@csrf_exempt
def backtest_view(request):
    if request.method == 'POST':
        form = BacktestForm(request.POST)
        if form.is_valid():
            symbol = form.cleaned_data['symbol']
            initial_investment = form.cleaned_data['initial_investment']
            short_moving_avg = form.cleaned_data['short_moving_avg']
            long_moving_avg = form.cleaned_data['long_moving_avg']

            result = backtest.run_backtest(symbol, initial_investment, short_moving_avg, long_moving_avg)
            return JsonResponse(result)

    else:
        form = BacktestForm()
        return form

@csrf_exempt
def view_predictions(request):
    if request.method == 'POST':
        symbol = request.POST['symbol']
        kagglehub.login()
        path = kagglehub.model_download("keras/gemma/keras/gemma_1.1_instruct_2b_en")
        model = joblib.load(path)
        
        # Fetch historical stock data for prediction
        stock_data = StockData.objects.filter(symbol=symbol).order_by('date')
    
        df = pd.DataFrame(list(stock_data.values('date', 'close_price')))
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        df['close_price'] = pd.to_numeric(df['close_price'])

        # Generate predictions for the next 30 days
        future_dates = pd.date_range(start=df.index[-1], periods=30, freq='D')
        future_predictions = model.predict(df['close_price'].values[-30:])

        # Store predictions in the database
        for i, date in enumerate(future_dates):
            actual_price_data = StockData.objects.filter(symbol=symbol, date=date).first()
            Prediction.objects.update_or_create(
                symbol=symbol,
                date=date,
                predicted_price= Decimal(future_predictions[i]),
                actual_price = Decimal(actual_price_data.close_price) if actual_price_data else None  
            )

        return JsonResponse({'symbol': symbol, 'predictions': future_predictions.tolist()})

    
@csrf_exempt
def generate_report(request):
    if request.method == 'POST':
        symbol = request.POST['symbol']
        backtest_results = BacktestResult.objects.filter(symbol=symbol)
        stock_data = StockData.objects.filter(symbol=symbol)
        predictions = Prediction.objects.filter(symbol=symbol)

        total_return, max_dropdown, number_of_trades = report.calculate_backtest_metrics(backtest_results)
        actual_prices = [data.close_price for data in stock_data]
        predicted_prices = [pred.price for pred in predictions]
        mae, rmse = report.calculate_prediction_metrics(actual_prices, predicted_prices)
    
        backtest_metrics = {
            'total_return': total_return,
            'max_dropdown': max_dropdown,
            'number_of_trades': number_of_trades
        }
        prediction_metrics = {
            'mae': mae,
            'rmse': rmse
        }


        stock_plot = report.generate_stock_price_plot(stock_data, predictions)
    
        if request.GET.get('format') == 'json':
            
            return JsonResponse({
                'backtest_metrics': backtest_metrics,
                'prediction_metrics': prediction_metrics
            })
    
        elif request.GET.get('format') == 'pdf':
           
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="backtest_report_{symbol}.pdf"'
        
           
            report.generate_pdf_report(response, backtest_metrics, prediction_metrics, stock_plot)
        
            return response

        return JsonResponse({
            'backtest_metrics': backtest_metrics,
            'prediction_metrics': prediction_metrics
        })
    