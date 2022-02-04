from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from cart.models import Cart


class CreateOrder(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        cart = Cart.objects.filter(cart_owner=request.data['cart_owner'])\
            .values('cart_item__product_id', 'cart_item__price', 'cart_item__cost', 'quantity')

        if cart.exists():
            # Create Order
            order_serializer = OrderSerializer(data={'customer': request.data['cart_owner']})
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
            data.append({order['order_no']: order_details})

        return Response(data)
