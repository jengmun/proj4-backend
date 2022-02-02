# from rest_framework import generics, permissions
# from rest_framework.response import Response
# from .models import Account
# from .serializers import UserSerializer


# class CreateAccount(generics.ListCreateAPIView):
#     permission_classes = (permissions.AllowAny,)
#     serializer_class = UserSerializer
#     queryset = Account.objects.all()
#
#     def post(self, request):
#         email = request.data.get("email", "")
#         first_name = request.data.get("first_name", "")
#         last_name = request.data.get("last_name", "")
#         address = request.data.get("address", "")
#         postal_code = request.data.get("postal_code", "")
#         password = request.data.get("password", "")
#
#         new_user = Account.objects.create_user(email=email, first_name=first_name, last_name=last_name, address=address, postal_code=postal_code, password=password)
#         return Response("created")


from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Account


class CreateAccount(APIView):
    def post(self, request):
        account = Account.objects.create_user(request.data['email'],
                                              request.data['first_name'],
                                              request.data['last_name'],
                                              request.data['address'],
                                              request.data['postal_code'],
                                              request.data['password'])

        return Response("Account created!")
