from django.urls import path
from . import views

app_name = "lists"
urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("lists/unique-list", views.view_list, name="view_list"),
]

