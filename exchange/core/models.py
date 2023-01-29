from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import random
from django.urls import reverse
from djongo import models
from decimal import Decimal
from djongo.models.fields import ObjectIdField
from bson.objectid import ObjectId

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    btc_balance = models.FloatField()
    usd_balance = models.FloatField()

    #the method is used to automatically assign a random balance between 1 and 10 BTC to a new registered user
    def save(self, *args, **kwargs):
        if self.btc_balance is None:
            self.btc_balance = round(random.uniform(1, 10), 5)
        if self.usd_balance is None:
            self.usd_balance = round(100, 2)
        super(Wallet, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user)

#each time a user is created, a Wallet object is created for that user
@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)


class Order(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    btc_amount = models.FloatField()
    btc_unit_price = models.FloatField()
    total_price = models.FloatField()
    type = models.CharField(max_length=4, choices=(("buy", "buy"), ("sell", "sell")), default='')
    status = models.CharField(max_length=10, choices=(("open", "open"), ("closed", "closed")), default='open')  
    created = models.DateTimeField(auto_now_add=True)

    #the method is used to calculate the total price of the order based on the quantity of BTC and the unit price
    def save(self, *args, **kwargs):
        self.total_price = self.btc_unit_price * self.btc_amount
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return self.created.strftime("%d/%m/%Y, %H:%M:%S")

class Transaction(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller')
    btc_amount = models.FloatField()
    btc_unit_price = models.FloatField()
    total_price = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_price = self.btc_unit_price * self.btc_amount
        super(Transaction, self).save(*args, **kwargs)
    
    @property
    def is_buyer(self):
        return self.buyer == self.request.user

    @property
    def is_seller(self):
        return self.seller == self.request.user

    def __str__(self):
        return self.timestamp.strftime("%d/%m/%Y, %H:%M:%S")