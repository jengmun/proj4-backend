from django.urls import path
from . import views


urlpatterns = [
    path('', views.OrderList.as_view()),
    path('create/', views.CreateOrder.as_view()),
]
