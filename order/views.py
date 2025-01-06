from django.utils.translation import gettext_lazy as _
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from product.models import Product
from .models import OrderItem, Order
from .serializers import OrderItemSerializer, OrderSerializer



class PendingCartView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        order, created = Order.objects.get_or_create(
            user=self.request.user,
            status=Order.StatusOrder.pending
        )
        return order


class AddToCartView(generics.CreateAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


    def create(self, request, *args, **kwargs):
        try:
            product = Product.objects.get(id=kwargs['product_id'])
        except Product.DoesNotExist:
            return Response({"detail": _("محصول یافت نشد.")}, status=status.HTTP_404_NOT_FOUND)

        mutable_data = request.data.copy()
        mutable_data['product'] = product.id

        serializer = self.get_serializer(data=mutable_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


class RemoveFromCartView(generics.DestroyAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    queryset = OrderItem.objects.select_related('product', 'order')
    lookup_field = 'id'

    def perform_destroy(self, instance):
        self.get_serializer().destroy(instance)


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": _("آیتم با موفقیت از سبد خرید حذف شد.")}, status=status.HTTP_200_OK)


class UserOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    


class AdminOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]
    queryset = Order.objects.select_related('user')
