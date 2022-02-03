from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Cart
from .serializers import CartSerializer


class CartList(APIView):
    def get(self, request):
        items = Cart.objects.filter(cart_owner__id=request.query_params['cart_owner'])\
            .values('cart_item', 'cart_item__name', 'cart_item__image', 'cart_item__price', 'quantity')
        # serializer = CartSerializer(items, many=True)
        return Response(items)


class UpdateCart(APIView):
    def post(self, request, pk):
        queryset = Cart.objects.filter(cart_item=pk, cart_owner=request.data['cart_owner'])
        if queryset.exists():
            item = Cart.objects.get(cart_item=pk, cart_owner=request.data['cart_owner'])
            serializer = CartSerializer(instance=item, data={**request.data, 'quantity': item.quantity + 1})

            if serializer.is_valid():
                serializer.save()
                return Response('Cart updated!')

            else:
                return Response(serializer.errors)

        else:
            serializer = CartSerializer(data={**request.data, 'quantity': 1})

            if serializer.is_valid():
                serializer.save()

                return Response(serializer.data)

            else:
                return Response(serializer.errors)

    def delete(self, request, pk):
        item = Cart.objects.get(cart_item=pk, cart_owner=request.query_params['cart_owner'])
        if item.quantity == 1:
            item.delete()

            return Response('Removed from cart!')

        else:
            serializer = CartSerializer(instance=item, data={'quantity': item.quantity - 1}, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response('Cart updated!')

            else:
                return Response(serializer.errors)


class DeleteFromCart(APIView):
    def delete(self, request, pk):
        item = Cart.objects.filter(cart_item=pk, cart_owner=request.query_params['cart_owner'])
        item.delete()

        return Response('Removed from cart!')
