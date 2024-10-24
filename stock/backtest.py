import pandas as pd
from .models import StockData, BacktestResult
import numpy as np
from decimal import Decimal
from django.http import JsonResponse

def run_backtest(symbol, initial_investment, short_moving_avg, long_moving_avg):
    # Fetch stock data from the database
    stock_data = StockData.objects.filter(symbol=symbol).order_by('date')
    
    if not stock_data.exists():
        return {'error': 'No stock data available for this symbol.'}

    # Convert stock data to a pandas DataFrame
    df = pd.DataFrame(list(stock_data.values('date', 'close_price')))
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    
    # Calculate the short_moving_avg-day and long_moving_avg-day moving averages
    df['short_moving_avg'] = df['close_price'].rolling(window=short_moving_avg).mean()
    df['long_moving_avg'] = df['close_price'].rolling(window=long_moving_avg).mean()

    # Remove rows where moving averages are NaN
    df.dropna(subset=['short_moving_avg', 'long_moving_avg'], inplace=True)

    cash = Decimal(initial_investment)
    stock_held = 0
    number_of_trades = 0
    max_drawdown = Decimal(0)
    peak_value = cash  # Keep track of the peak portfolio value

    # Initialize buy/sell flag
    bought = False

    for i, row in df.iterrows():
        price = Decimal(row['close_price'])
        
        # Buy condition (price goes below short_moving_avg-day moving average and we haven't bought)
        if price < row['short_moving_avg'] and not bought:
            stock_held = cash / price
            cash = Decimal(0)  # Spent all the cash to buy stocks
            bought = True
            number_of_trades += 1

        # Sell condition (price goes above long_moving_avg-day moving average and we are holding stock)
        elif price > row['long_moving_avg'] and bought:
            cash = stock_held * price
            stock_held = 0
            bought = False
            number_of_trades += 1

        # Calculate the peak portfolio value (used for max drawdown calculation)
        current_value = cash + (stock_held * price)
        if current_value > peak_value:
            peak_value = current_value

        # Calculate drawdown
        drawdown = (peak_value - current_value) / peak_value * 100
        if drawdown > max_drawdown:
            max_drawdown = drawdown

    # If we're still holding stock at the end, sell it
    if stock_held > 0:
        cash = stock_held * price

    # Calculate total return
    total_return = ((cash - Decimal(initial_investment)) / Decimal(initial_investment)) * Decimal(100)
    final_value = cash

    # Store the backtest result in the database
    try:
        BacktestResult.objects.create(
        symbol=symbol,
        initial_investment=Decimal(initial_investment),
        total_return=total_return,
        max_dropdown=max_drawdown,
        final_value=final_value,
        number_of_trades=number_of_trades
    )
        return {
        'total_return': total_return,
        'final_value': final_value,
        'max_drawdown': max_drawdown,
        'number_of_trades': number_of_trades  # Removed duplicate 'final_value'
        }
    except:
        return JsonResponse("Something went wrong", safe=False)

    
