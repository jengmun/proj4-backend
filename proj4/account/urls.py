from django.urls import path
from . import views


urlpatterns = [
    path("create-account/", views.CreateAccount.as_view()),
]


