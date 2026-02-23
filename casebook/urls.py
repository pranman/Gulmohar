from django.urls import path

from . import views

urlpatterns = [
    path("", views.casebook_index, name="casebook_index"),
    path("new/", views.casebook_create, name="casebook_create"),
    path("<slug:slug>/", views.casebook_detail, name="casebook_detail"),
    path("<slug:slug>/edit/", views.casebook_edit, name="casebook_edit"),
]
