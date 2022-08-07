from django.urls import path

from . import views

urlpatterns = [
    path("", views.indexpage, name="indexpage"),
    path("wiki/<str:entrypage>", views.entrypage, name="entrypage"),
    path("newEntrypage", views.newEntrypage, name="newEntrypage"),
    path("wiki/<str:entrypage>/editpage", views.editpage, name="editpage"),
    path("randompage", views.randompage, name="randompage"),
    path("usersearch", views.usersearch, name="search"),
    path("Home", views.Home, name="Home")
]
