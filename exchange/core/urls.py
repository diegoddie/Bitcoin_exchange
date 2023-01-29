from . import views
from django.urls import path
from .views import ActiveOrdersView, CreateOrderView, OrderDeleteView, ProfitAndLossView, TransactionsListView

urlpatterns = [
    path('', views.home, name="home"),
    path('create-order/', CreateOrderView.as_view(), name="create_order"),
    path('active-orders/', ActiveOrdersView.as_view(), name='active_orders'),
    path('delete_order/<str:pk>/', OrderDeleteView.as_view(), name='delete_order'),
    path('transactions/', TransactionsListView.as_view(), name='transactions'),
    path('profit_and_loss/', ProfitAndLossView.as_view(), name='profit_and_loss')
]