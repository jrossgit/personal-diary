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
from app import api_views, htmx_views, views

from django.contrib.auth import views as auth_views
from django.urls import include, path


urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),

    path("", views.home_view, name="home"),
    path("todo", views.create_todo, name="todo-create"),
    path("todocategory/<uuid:category_id>/todo", views.create_todo, name="todo-create"),

    path("todocategory", views.create_todo_category, name="todo-category-create"),

    path("diary", views.create_update_diary_entry, name="diary-create-update"),

    path("htmx:delete", htmx_views.delete_element, name="htmx-delete-element"),

    path("htmx/todo/<uuid:todo_id>:delete", htmx_views.complete_todo, name="htmx-todo-complete"),
    path("htmx/todo/<uuid:todo_id>:form", htmx_views.create_todo_htmx_form, name="htmx-todo-card-form"),
    path("htmx/todo/<uuid:todo_id>", htmx_views.todo_htmx, name="htmx-todo"),
    path("htmx/todocategory/:form", htmx_views.create_todo_htmx_form, name="htmx-todo-card-form"),
    path("htmx/todocategory/<uuid:category_id>:form", htmx_views.create_todo_htmx_form, name="htmx-todo-card-form"),
    path("htmx/todocategory/<uuid:id>:delete", htmx_views.delete_todo_category, name="htmx-todo-category-delete"),

    path("htmx/diary/<uuid:diary_entry_id>:form", htmx_views.create_diary_entry_htmx_form, name="htmx-diary-entry-create-form"),
    path("htmx/diary/:form", htmx_views.create_diary_entry_htmx_form, name="htmx-diary-entry-create-form"),

    path("__debug__/", include("debug_toolbar.urls")),
]

urlpatterns.extend([
    path("api/brainworms", api_views.create_brainworm_todo, name="brainworms"),
])
