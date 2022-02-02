from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Account, Cart
from .serializers import CartSerializer


class CreateAccount(APIView):
    def post(self, request):
        account = Account.objects.create_user(request.data['email'],
                                              request.data['first_name'],
                                              request.data['last_name'],
                                              request.data['address'],
                                              request.data['postal_code'],
                                              request.data['password'])

        return Response("Account created!")


class AddToCart(APIView):
    def post(self, request):
        serializer = CartSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        else:
            return Response(serializer.errors)
