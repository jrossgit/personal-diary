
from app.htmx import views
from django.urls import path


urlpatterns = [
    path("home/completed_today", views.TaskCountTodayHTMXView.as_view(), name="htmx-todo-count-today"),

    path("diary/:form", views.DiaryCreateFormHTMXView.as_view(), name="htmx-diary-entry-create-form"),
    path("diary/<uuid:pk>:form", views.DiaryCreateFormHTMXView.as_view(), name="htmx-diary-entry-create-form"),

    path("todocategory:form", views.TaskCreateFormHTMXView.as_view(), name="htmx-todo-card-form"),
    path("todocategory/<uuid:category_pk>:form", views.TaskCreateFormHTMXView.as_view(), name="htmx-todo-card-form"),
    path("todocategory/<uuid:pk>:delete", views.htmx_delete_todo_category_view, name="htmx-todo-category-delete"),

    path("todo/<uuid:todo_id>:form", views.TaskCreateFormHTMXView.as_view(), name="htmx-todo-card-form"),
    path("todo/<uuid:todo_id>", views.TaskRetrieveHTMXView.as_view(), name="htmx-todo"),
    path("todo/<uuid:todo_id>:delete", views.htmx_complete_todo, name="htmx-todo-complete"),

    path(":delete", views.htmx_delete_element, name="htmx-delete-element"),
]
