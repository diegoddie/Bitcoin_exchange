from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    type = forms.ChoiceField(choices=(('buy', 'buy'), ('sell', 'sell')), required=True)
    btc_amount = forms.FloatField(required=True)
    btc_unit_price = forms.FloatField(required=True)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(OrderCreateForm, self).__init__(*args, **kwargs)
    
    #The clean method verifies the availability of funds and quantities of available bitcoins before creating an order.
    def clean(self):
        cleaned_data = super().clean()
        btc_amount = cleaned_data.get("btc_amount")
        btc_unit_price = cleaned_data.get("btc_unit_price")
        type = cleaned_data.get("type")
        total_price = btc_amount*btc_unit_price
        
        if type == 'buy' and float(self.user.wallet.usd_balance) < total_price:
            raise forms.ValidationError("Insufficient funds")
        
        if type == 'sell' and btc_amount > float(self.user.wallet.btc_balance):
            raise forms.ValidationError("You cannot sell more BTC than you have")

    class Meta:
        model = Order
        fields = ['btc_amount', 'btc_unit_price', 'type']