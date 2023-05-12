import datetime

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.forms import HiddenInput
from django.shortcuts import render, redirect, reverse
from django.views.generic import FormView, TemplateView

from app import forms, models


class HTMXTemplateMixin:
    """
    Strips
    """
    def get_template_names(self):
        if "component" not in self.request.GET:
            raise NotImplementedError("HTMX call should define a component to return")
        return [f"components/{self.request.GET['component']}.html"]


class TaskCountTodayHTMXView(HTMXTemplateMixin, TemplateView):

    def get_context_data(self, **kwargs):
        return {"number": models.models.Todo.objects.completed_today().count()}


# TODO: add HTMX handling to this class
class TaskCreateFormHTMXView(FormView):

    def get(self, request, *args, **kwargs):
        if "todo_id" in kwargs:
            form = forms.NewTodoForm(instance=models.Todo.objects.get(id=kwargs["todo_id"]))
        else:
            form = forms.NewTodoForm(initial={"category": kwargs["category_id"]})

        form.fields["category"].widget = HiddenInput()

        return render(
            request,
            "components/todos/card_todo_create.html",
            context={"form": form, "todo_id": kwargs.get("todo_id")}
        )

    def post(self, request, *args, **kwargs):
        if "todo_id" in kwargs:
            form = forms.NewTodoForm(request.POST, instance=models.Todo.objects.get(id=kwargs["todo_id"]))
        else:
            form = forms.NewTodoForm(request.POST)
        todo = form.save()

        return render(
            request,
            "components/todos/card_todo.html",
            context={"todo": todo}
        )


