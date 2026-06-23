from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/champions/", views.champions_api, name="champions_api"),
    path("api/participants/", views.participants_api, name="participants_api"),
    path("api/item-frequencies/", views.item_frequencies_api, name="item_frequencies_api"),
]
