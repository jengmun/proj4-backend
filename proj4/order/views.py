from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from cart.models import Cart
from inventory.models import Inventory
from inventory.serializers import InventorySerializer


class CreateOrder(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        cart = Cart.objects.filter(cart_owner=request.data['cart_owner'])\
            .values('cart_item__product_id', 'cart_item__price', 'cart_item__cost', 'quantity')

        if cart.exists():
            # Create Order
            order_serializer = OrderSerializer(data={'customer': request.data['cart_owner'], 'total': request.data['total']})
            if order_serializer.is_valid():
                order_serializer.save()
                order_no = (order_serializer.data['order_no'])

            else:
                return Response(order_serializer.errors)

            # Create Order Item
            for cart_item in cart:
                order_item_serializer = OrderItemSerializer(data={'price': cart_item['cart_item__price'],
                                                                  'cost': cart_item['cart_item__cost'],
                                                                  'quantity': cart_item['quantity'],
                                                                  'item': cart_item['cart_item__product_id'],
                                                                  'order': order_no})
                if order_item_serializer.is_valid():
                    order_item_serializer.save()

                else:
                    return Response(order_item_serializer.errors)

            # Decrease quantity from inventory
            for cart_item in cart:
                inventory = Inventory.objects.get(product_id=cart_item['cart_item__product_id'])
                inventory_serializer = InventorySerializer(instance=inventory, data={'quantity': inventory.quantity - cart_item['quantity']}, partial=True)

                if inventory_serializer.is_valid():
                    inventory_serializer.save()

                else:
                    return Response(inventory_serializer.errors)

            # Delete items from cart
            Cart.objects.filter(cart_owner=request.data['cart_owner']).delete()

            return Response('Order created!')

        return Response('Order not created.')


class OrderList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        data = []
        orders = Order.objects.filter(customer=request.query_params['cart_owner'])
        order_serializer = OrderSerializer(orders, many=True)

        for order in order_serializer.data:
            order_details = OrderItem.objects.filter(order_id=order['order_no']).values('item__name', 'item__image', 'quantity', 'price')
            data.append({'order_no': order['order_no'], 'details': order_details, 'total': order['total'], 'date': order['date']})

        return Response(data)


class GetAllOrders(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        orders = OrderItem.objects.all().values('item__name', 'quantity', 'price', 'order__date', 'order__total')

        return Response(orders)
