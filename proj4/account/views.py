from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Account
from .serializers import UserSerializer


class CreateAccount(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            account = Account.objects.create_user(serializer.data['email'],
                                                  serializer.data['first_name'],
                                                  serializer.data['last_name'],
                                                  serializer.data['address'],
                                                  serializer.data['postal_code'],
                                                  serializer.data['password'])

            return Response(account)

        else:
            return Response(serializer.errors)
