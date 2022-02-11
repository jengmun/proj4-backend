from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Inventory
from .serializers import InventorySerializer


class InventoryList(APIView):
    def get(self, request):
        inventory = Inventory.objects.all()
        serializer = InventorySerializer(inventory, many=True)

        return Response(serializer.data)


class InventoryDetails(APIView):
    def get(self, request, pk):
        inventory = Inventory.objects.get(product_id=pk)
        serializer = InventorySerializer(inventory)

        return Response(serializer.data)


class AddInventory(APIView):
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = InventorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response('Inventory added!')

        else:
            return Response(serializer.errors)


class UpdateInventory(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        inventory = Inventory.objects.get(product_id=pk)
        serializer = InventorySerializer(instance=inventory, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response('Inventory updated!')

        else:
            return Response(serializer.errors)


class DeleteInventory(APIView):
    # permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        inventory = Inventory.objects.get(product_id=pk)
        inventory.delete()

        return Response('Inventory deleted!')
