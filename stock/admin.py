from django.contrib import admin
from .models import StockData
from .models import BacktestResult
from .models import Prediction
# Register your models here.

admin.site.register(StockData)
admin.site.register(BacktestResult)
admin.site.register(Prediction)