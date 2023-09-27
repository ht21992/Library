from django.urls import path
from . import views

app_name = "frontend"

urlpatterns = [
    path("", views.main, name="mainView"),
    path("partials/", views.get_objects_partials, name="get_objects_partials"),
]
