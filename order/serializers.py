from rest_framework.serializers import ModelSerializer
from .models import Order, OrderItem


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'price', 'color', 'quantity']
        read_only_fields = ['price']


    def create(self, validated_data):
        user = self.context['request'].user

        order, created = Order.objects.get_or_create(
            user=user,
            status=Order.StatusOrder.pending
        )

        product = validated_data['product']
        order_item, created = OrderItem.objects.get_or_create(
            order=order,
            product=product,
            defaults={
                'price': product.price,
                'color': validated_data.get('color', ''),
                'quantity': validated_data.get('quantity', 1)
            }
        )

        if not created:
            order_item.quantity += int(validated_data.get('quantity', 1))
            order_item.save()

        order.total_price += product.price * int(validated_data.get('quantity', 1))
        order.save()

        return order_item

    def destroy(self, instance):
        order = instance.order
        order.total_price -= instance.price * instance.quantity
        order.save()
        instance.delete()



class OrderSerializer(ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'status', 'total_price', 'payment_date', 'is_paid', 'first_name', 'last_name',
            'email', 'phone_number', 'state', 'city', 'zip_code', 'address', 'order_items'
        ]
        read_only_fields = ['user', 'status', 'total_price', 'payment_date', 'is_paid'] 
