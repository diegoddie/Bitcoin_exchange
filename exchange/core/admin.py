from django.contrib import admin
from .models import Wallet, Order, Transaction

admin.site.register(Wallet)
admin.site.register(Order)
admin.site.register(Transaction)

