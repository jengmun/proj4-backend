from datetime import date
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


class OrderAnalytics(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        orders = Order.objects.values('date', 'total', 'customer')
        order_items = OrderItem.objects.values('item__name', 'item__image', 'quantity', 'price', 'cost')

        # Compute Revenue
        revenue = 0
        for order in orders:
            revenue += order['total']

        # Compute COGS
        cost = 0
        for item in order_items:
            cost += item['cost'] * item['quantity']

        # Compute Gross Profit
        gross_profit = revenue - cost

        # Compute Gross Profit Margin
        gpm = round(gross_profit/revenue, 2)

        # Compute Revenue, COGS, Gross Profit, GPM per product, sorted by Highest Quantity Sold
        highest_quantity = {}
        for item in order_items:
            if item['item__name'] in highest_quantity:
                highest_quantity[item['item__name']]['quantity'] += item['quantity']
                highest_quantity[item['item__name']]['revenue'] += item['price'] * item['quantity']
                highest_quantity[item['item__name']]['cost'] += item['cost'] * item['quantity']

            else:
                highest_quantity[item['item__name']] = {'quantity': item['quantity'],
                                                        'revenue': item['price'] * item['quantity'],
                                                        'cost': item['cost'] * item['quantity'],
                                                        'image': item['item__image']}

            highest_quantity[item['item__name']]['gross_profit'] = highest_quantity[item['item__name']]['revenue'] - highest_quantity[item['item__name']]['cost']
            highest_quantity[item['item__name']]['gpm'] = highest_quantity[item['item__name']]['gross_profit'] / highest_quantity[item['item__name']]['revenue']

        sorted_quantity = sorted(highest_quantity.items(), key=lambda x: x[1]['quantity'], reverse=True)

        sanitised_object = []
        for item in sorted_quantity:
            sanitised_object.append({'name': item[0], 'quantity': item[1]['quantity'],
                                     'revenue': item[1]['revenue'],
                                     'cost': item[1]['cost'],
                                     'gross_profit': item[1]['gross_profit'],
                                     'gpm': item[1]['gpm'],
                                     'image': item[1]['image']})

        # Sanitise Date and Compute Total Revenue per day
        orders_by_date = []

        # check if the order date exists in orders_by_date list
        def is_exists():
            for elem in orders_by_date:
                if elem['date'] == order_date:
                    index = orders_by_date.index(elem)
                    return {'exists': True, 'index': index}

            return {'exists': False}

        # for each order
        for order in orders:
            order_date = order['date'].date()

            # check if the order date exists in orders_by_date list
            if len(orders_by_date) == 0:
                orders_by_date.append({'total': order['total'], 'date': order_date})

            else:
                if is_exists()['exists']:
                    orders_by_date[is_exists()['index']]['total'] += order['total']

                else:
                    orders_by_date.append({'total': order['total'], 'date': order_date})

        return Response({'revenue': revenue, 'cost': cost, 'gross_profit': gross_profit, 'gpm': gpm, 'sorted_quantity': sanitised_object, 'orders': orders_by_date})

