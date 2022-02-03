from django.urls import path
from . import views

urlpatterns = [
    path('', views.CartList.as_view()),
    path('update-cart/<str:pk>/', views.UpdateCart.as_view()),
    path('remove-from-cart/<str:pk>/', views.DeleteFromCart.as_view()),
]

