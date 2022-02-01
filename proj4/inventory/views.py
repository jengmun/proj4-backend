from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Inventory
from .serializers import InventorySerializer


class InventoryList(APIView):
    def get(self, request):
        inventory = Inventory.objects.all()
        serializer = InventorySerializer(inventory, many=True)

        return Response(serializer.data)


class AddInventory(APIView):
    def post(self, request):
        serializer = InventorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response('Inventory added!')

        else:
            return Response('Error: Inventory not added.')


