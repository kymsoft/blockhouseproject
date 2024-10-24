from django.db import models
# Create your models here.

class StockData(models.Model):
    open_price = models.DecimalField(max_digits=12, decimal_places=2)
    close_price = models.DecimalField(max_digits=12, decimal_places=2)
    high_price = models.DecimalField(max_digits=12, decimal_places=2)
    low_price = models.DecimalField(max_digits=12, decimal_places=2)
    volume = models.IntegerField()
    symbol = models.CharField(max_length=10)
    date = models.CharField(max_length=20)
    
    class Meta:
        ordering = ['-date']

class BacktestResult(models.Model):
    symbol = models.CharField(max_length=10)
    initial_investment = models.DecimalField(max_digits=12, decimal_places=2)
    total_return = models.DecimalField(max_digits=12, decimal_places=2)
    final_value = models.DecimalField(max_digits=12, decimal_places=2)
    max_dropdown = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    number_of_trades = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Backtest {self.symbol} - Return: {self.total_return}%"


class Prediction(models.Model):
    symbol = models.CharField(max_length=10)
    date = models.DateField()
    predicted_price = models.DecimalField(max_digits=10, decimal_places=2)
    actual_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']
    def __str__(self):
        return f"{self.symbol} - Prediction for {self.date}"
