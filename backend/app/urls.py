"""URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path("", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path("", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path("blog/", include("blog.urls"))
"""
from app import views
from app.api import views as api_views

from django.urls import include, path


urlpatterns = [

    path("accounts/", include("django.contrib.auth.urls")),
    path("logout", views.logout_view, name="log-out"),
    path("", views.home_view, name="home"),
    path("todo", views.create_todo, name="todo-create"),
    path("todocategory/<uuid:category_id>/todo", views.create_todo, name="todo-create"),
    path("todocategory", views.create_todo_category, name="todo-category-create"),
    path("diary", views.create_update_diary_entry, name="diary-create-update"),
    path("__debug__/", include("debug_toolbar.urls")),
]

urlpatterns.extend(
    [
        path("api/categories", api_views.list_todo_categories, name="list-todo-categories"),
        path("api/categories/<uuid:category_id>/todos", api_views.create_todo, name="create-todo"),
    ]
)

urlpatterns.extend([path("htmx/", include("app.htmx.urls"))])
