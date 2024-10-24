import numpy as np
from io import BytesIO
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def calculate_backtest_metrics(backtest_results):
    total_return = backtest_results.total_return
    max_dropdown = backtest_results.max_dropdown
    number_of_trades = backtest_results.number_of_trades
    return total_return, max_dropdown, number_of_trades

def calculate_prediction_metrics(actual_prices, predicted_prices):
    actual = np.array(actual_prices)
    predicted = np.array(predicted_prices)
    mean_absolute_error = np.mean(np.abs(actual - predicted))
    rmse = np.sqrt(np.mean((actual - predicted) ** 2))
    return mean_absolute_error, rmse

def generate_stock_price_plot(stock_data, predictions):
    plt.figure(figsize=(10, 6))
    dates = [data.date for data in stock_data]
    actual_prices = [data.close_price for data in stock_data]
    predicted_prices = [pred.price for pred in predictions]
    
    plt.plot(dates, actual_prices, label='Actual Prices', color='blue')
    plt.plot(dates, predicted_prices, label='Predicted Prices', color='green')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Stock Prices: Actual vs Predicted')
    plt.legend()
    
    # Save plot to a BytesIO object to serve it in response
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    return buffer


def generate_pdf_report(response, backtest_metrics, prediction_metrics, stock_plot):
    
    pdf = canvas.Canvas(response, pagesize=letter)
    
    # Write some text
    pdf.drawString(100, 750, "Backtest Report")
    pdf.drawString(100, 730, f"Total Return: {backtest_metrics['total_return']}")
    pdf.drawString(100, 710, f"Max Drawdown: {backtest_metrics['max_dropdown']}")
    pdf.drawString(100, 690, f"Number of Trades: {backtest_metrics['number_of_trades']}")
    
    pdf.drawString(100, 650, "Prediction Metrics")
    pdf.drawString(100, 630, f"Mean Absolute Error: {prediction_metrics['mae']}")
    pdf.drawString(100, 610, f"RMSE: {prediction_metrics['rmse']}")
    
    # Insert stock price plot
    pdf.drawImage(stock_plot, 100, 400, width=400, height=200)
    
    pdf.save()