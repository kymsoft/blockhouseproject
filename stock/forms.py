from django import forms

# Form for Backtesting
class BacktestForm(forms.Form):
    # Define the stock symbol input field
    symbol = forms.CharField(
        max_length=10,
        label="Stock Symbol",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter stock symbol, e.g., AAPL',
            'required': True
        })
    )

    # Define the initial investment input field
    initial_investment = forms.DecimalField(
        label="Initial Investment",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '10000',
            'required': True
        })
    )

    # Define the short moving average window input field (default to 50-day)
    short_moving_avg = forms.IntegerField(
        label="Short Moving Average (days)",
        initial=50,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '50',
            'required': True
        })
    )

    # Define the long moving average window input field (default to 200-day)
    long_moving_avg = forms.IntegerField(
        label="Long Moving Average (days)",
        initial=200,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '200',
            'required': True
        })
    )
