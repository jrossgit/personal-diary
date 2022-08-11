import datetime

from django.shortcuts import render, redirect, reverse

from app import forms, models


def home_view(request):
    unsorted_todos = models.Todos.objects.filter(
        complete_time__isnull=True,
        category__isnull=True)
    sorted_todos = models.Todos.objects.filter(
        complete_time__isnull=True,
        category__isnull=False
    ).order_by("category__name")

    return render(request, template_name="home.html", context={
        "sorted_todos": sorted_todos,
        "unsorted_todos": unsorted_todos,
        "form": forms.NewTodoForm(),
    })


def create_todo(request, category_id=None):
    if request.method == "GET":

        initial = {}
        if category_id:
            initial["category"] = models.TodoCategory.objects.get(id=category_id).id

        new_todo_form = forms.NewTodoForm(initial=initial)
        return render(request, template_name="create_todo.html", context={
            "form": new_todo_form,
        })
    elif request.method == "POST":
        form = forms.NewTodoForm(request.POST)
        form.save()
        return redirect("home")


def create_todo_category(request):
    if request.method == "GET":
        return render(request, template_name="create_todo_category.html", context={
            "form": forms.NewTodoCategoryForm(),
        })
    elif request.method == "POST":
        form = forms.NewTodoCategoryForm(request.POST)
        form.save()
        return redirect("home")


def complete_todo(request, id):
    todo = models.Todos.objects.get(id=id)
    if not todo.complete_time:
        todo.complete_time = datetime.datetime.now()
        todo.save()

    if todo.category:
        return redirect(f"{reverse('home')}#{todo.category.card_slug}")
    else:
        return redirect("home")
