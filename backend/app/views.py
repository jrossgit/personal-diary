import datetime

from django.shortcuts import render, redirect

from app import forms, models


def home_view(request):
    displayed_todos = models.Todos.objects.exclude(
        complete_time__isnull=False,
    )

    return render(request, template_name="home.html", context={
        "todos": displayed_todos,
        "form": forms.NewTodoForm(),
    })


def create_todo(request):
    if request.method == "GET":
        return render(request, template_name="create_todo.html", context={
            "form": forms.NewTodoForm(),
        })
    elif request.method == "POST":
        form = forms.NewTodoForm(request.POST)
        form.save()
        return redirect("home")


def complete_todo(request, id):
    todo = models.Todos.objects.get(id=id)
    if not todo.complete_time:
        todo.complete_time = datetime.datetime.now()
        todo.save()
    return redirect("home")
