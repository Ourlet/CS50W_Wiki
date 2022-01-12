from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry-page"),
    path("results", views.search, name="search-result"),
    path("create", views.create, name="create-entry"),
    path("save", views.save, name="save-entry"),
    path("edit", views.edit, name="edit-entry"),
    path("save-edit", views.saveEdit, name="save-edit-entry"),
    path("random", views.random, name="random"),
]
