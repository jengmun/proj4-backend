from django.urls import path
from . import views


urlpatterns = [
    path('', views.InventoryList.as_view()),
    path('add-inventory/', views.AddInventory.as_view()),
    path('update-inventory/<str:pk>/', views.UpdateInventory.as_view()),
    path('delete-inventory/<str:pk>/', views.DeleteInventory.as_view()),
    path('<str:pk>/', views.InventoryDetails.as_view())
]
