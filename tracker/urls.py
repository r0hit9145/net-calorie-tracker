from django.urls import path
from . import views

urlpatterns = [
    path("", views.user_list, name="user_list"),
    path("users/new/", views.user_create, name="user_create"),
    path("users/<int:user_id>/", views.user_detail, name="user_detail"),
    path("users/<int:user_id>/delete/", views.user_delete, name="user_delete"),
]


