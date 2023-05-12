
from app.htmx import views
from django.urls import path


urlpatterns = [
    path("home/completed_today", views.TaskCountTodayHTMXView.as_view(), name="htmx-todo-count-today"),

    path("todocategory/:form", views.TaskCreateFormHTMXView.as_view(), name="htmx-todo-card-form"),
    path("todocategory/<uuid:category_id>:form", views.TaskCreateFormHTMXView.as_view(), name="htmx-todo-card-form"),
    path("todo/<uuid:todo_id>:form", views.TaskCreateFormHTMXView.as_view(), name="htmx-todo-card-form"),
]
