from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Account
from .serializers import UserSerializer


class CreateAccount(APIView):
    def post(self, request):
        account = Account.objects.create_user(request.data['email'],
                                              request.data['first_name'],
                                              request.data['last_name'],
                                              request.data['address'],
                                              request.data['postal_code'],
                                              request.data['password'])

        return Response("Account created!")


class GetAccountDetails(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, email):
        account = Account.objects.get(email=email)
        serializer = UserSerializer(account)

        return Response(serializer.data)
