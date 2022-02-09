from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.entries, name="entries"),
    path("wiki/<str:name>/<str:mode>",views.edit,name="edit")
    ]
