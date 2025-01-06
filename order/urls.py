from django.urls import path
from .views import AddToCartView, RemoveFromCartView, UserOrderListView, AdminOrderListView, PendingCartView


app_name = 'order'

urlpatterns = [
    path('', PendingCartView.as_view(), name='pending-cart'),
    path('add-to-cart/<int:product_id>/', AddToCartView.as_view(), name='add-to-cart'),
    path('remove-from-cart/<int:id>/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('user-orders/', UserOrderListView.as_view(), name='user-orders'),
    path('admin-orders/', AdminOrderListView.as_view(), name='admin-orders'),
]
