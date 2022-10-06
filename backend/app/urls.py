"""coasters URL Configuration

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
from app import htmx_views, views

from django.urls import include, path


urlpatterns = [
    path("", views.home_view, name="home"),
    path("todo", views.create_todo, name="todo-create"),
    path("todo/<uuid:id>/complete", views.complete_todo, name="todo-complete"),
    path("todocategory/<uuid:category_id>/todo", views.create_todo, name="todo-create"),

    path("todocategory", views.create_todo_category, name="todo-category-create"),
    path("todocategory/<uuid:id>/delete", views.delete_todo_category, name="todo-category-delete"),

    path("diary", views.create_update_diary_entry, name="diary-create-update"),

    path("htmx/todo/<uuid:todo_id>:form", htmx_views.create_todo_htmx_form, name="htmx-todo-card-form"),
    path("htmx/todocategory/:form", htmx_views.create_todo_htmx_form, name="htmx-todo-card-form"),
    path("htmx/todocategory/<uuid:category_id>:form", htmx_views.create_todo_htmx_form, name="htmx-todo-card-form"),

    path("__debug__/", include("debug_toolbar.urls")),
]
