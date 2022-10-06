from django.shortcuts import render

from django.forms import HiddenInput

from app.forms import NewTodoForm
from app.models import Todos


def create_todo_htmx_form(request, category_id=None, todo_id=None):

    if request.method == "GET":
        if todo_id:
            form = NewTodoForm(instance=Todos.objects.get(id=todo_id))
        else:
            form = NewTodoForm(initial={"category": category_id})

        form.fields["category"].widget = HiddenInput()

        return render(
            request,
            "components/todos/card_todo_create.html",
            context={"form": form}
        )

    elif request.method == "POST":
        form = NewTodoForm(request.POST)
        todo = form.save()
        return render(
            request,
            "components/todos/card_todo.html",
            context={"todo": todo})
