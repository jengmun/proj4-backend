from django.urls import path
from . import views


urlpatterns = [
    path("", views.InventoryList.as_view()),
    path("add-inventory/", views.AddInventory.as_view())
]
