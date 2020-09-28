from django.urls import path

from . import views
app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="title"),
    path("search", views.search, name = "search"),
    path("create", views.create_page, name = "create"),
    path("creating", views.creating, name = "creating"),
    path('random', views.random_list, name = "random"),
    path('edit/<str:title>', views.edit, name = "edit"),
    path('after_edit/<str:title>', views.after_edit, name = "after_edit")
]
