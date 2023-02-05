from django.shortcuts import render
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import DeleteView
from .forms import OrderCreateForm
from bson import ObjectId
from .models import Order, Wallet, Transaction
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from mongoengine import ObjectIdField
from django.contrib.auth.models import User
from .utils import get_btc_data
import datetime
from django.contrib import messages
from django.views import View
from django.db.models import Q

btc_usd_price = None
btc_usd_change = None
last_update = None

def calculate_profit_loss(user):
    transactions = Transaction.objects.filter(Q(buyer=user) | Q(seller=user))
    profit_loss = 0
    for transaction in transactions:
        if transaction.buyer == user:
            profit_loss -= transaction.total_price
        else:
            profit_loss += transaction.total_price
    return profit_loss

def update_prices():
    global btc_usd_price, btc_usd_change, last_update
    now = datetime.datetime.now()
    if last_update is None or (now - last_update).total_seconds() > 900:
        # Aggiorna i prezzi solo se sono passati 30 minuti dall'ultimo aggiornamento
        btc_usd_price, btc_usd_change = get_btc_data()
        last_update = now

def home(request):
    if not request.user.is_authenticated:
        return render(request, "core/home.html")
    update_prices()
    user = request.user
    wallet = Wallet.objects.get(user=user)
    last_transactions = Transaction.objects.filter(Q(buyer=user) | Q(seller=user)).order_by('-timestamp')[:3]
    context = {
        'wallet': wallet,
        'profit_loss': calculate_profit_loss(user),
        'btc_usd_price': btc_usd_price,
        'btc_usd_change': btc_usd_change,
        'last_transactions': last_transactions,
    }
    return render(request, "core/home.html", context)

def match_orders(order):
    match = False
    open_orders = Order.objects.filter(status='open').order_by('btc_unit_price').exclude(author=order.author)
    for open_order in open_orders:
        if open_order.type != order.type and open_order.btc_unit_price >= order.btc_unit_price:
            transaction_amount = min(order.btc_amount, open_order.btc_amount)
            transaction = Transaction.objects.create(
                buyer=order.author,
                seller=open_order.author,
                btc_amount=transaction_amount,
                btc_unit_price=open_order.btc_unit_price
            )
            # update wallets
            order.author.wallet.btc_balance += transaction.btc_amount
            order.author.wallet.usd_balance -= transaction.total_price
            order.author.wallet.save()
            open_order.author.wallet.btc_balance -= transaction.btc_amount
            open_order.author.wallet.usd_balance += transaction.total_price
            open_order.author.wallet.save()

            # update order status
            order.btc_amount -= transaction_amount
            open_order.btc_amount -= transaction_amount
            if order.btc_amount <= 0:
                order.status = 'closed'
            if open_order.btc_amount <= 0:
                open_order.status = 'closed'
            order.save()
            open_order.save()
            match = True

            # check if there's still room for matching
            if order.btc_amount > 0:
                match_orders(order)
            break
    return match

class CreateOrderView(LoginRequiredMixin, CreateView):
    model = Order
    template_name = 'core/create_order.html'
    success_url = '.'
    form_class = OrderCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        match = match_orders(form.instance)
        if match:
            messages.success (self.request, "Order matched")
        else:
            messages.error(self.request, "Order unmatched")
        return super().form_valid(form)
    
    #the method is passing the argument 'user' (which is the current user) to the OrderCreateForm form constructor. In this way, the form can use this argument to perform custom validation checks on the data entered by the user.
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

class ActiveOrdersView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'core/active_orders.html'

    def get_queryset(self):
        queryset = Order.objects.filter(status ='open').order_by('-created')
        if not self.request.user.is_superuser:
            queryset = queryset.filter(author=self.request.user)
        return queryset


class OrderDeleteView(LoginRequiredMixin, DeleteView):
    model = Order
    template_name = 'core/delete_order.html'
    success_url = reverse_lazy('active_orders')

    def get_object(self, queryset=None):
        try:
            return Order.objects.get(_id=ObjectId(self.kwargs.get('pk')))
        except Order.DoesNotExist:
            raise Http404("No Order found matching the query")


class TransactionsListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'core/transactions.html'

    def get_queryset(self):
        queryset = Transaction.objects.filter(Q(buyer=self.request.user) | Q(seller=self.request.user)).order_by('-timestamp')
        return queryset

class ProfitAndLossView(LoginRequiredMixin, View):
    template_name = 'core/profit_and_loss.html'

    def get(self, request, *args, **kwargs):
        profit_loss = calculate_profit_loss(request.user)
        return render(request, self.template_name, {'profit_loss': profit_loss})

