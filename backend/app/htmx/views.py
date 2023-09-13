import datetime

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.forms import HiddenInput
from django.shortcuts import HttpResponse, render, redirect, reverse
from django.views.generic import DeleteView, FormView, TemplateView

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
        return {"number": models.Todo.objects.completed_today().count()}


# TODO: add HTMX handling to this class
class TaskCreateFormHTMXView(FormView):

    def get(self, request, *args, **kwargs):
        if "todo_id" in kwargs:
            form = forms.NewTodoForm(instance=models.Todo.objects.get(id=kwargs["todo_id"]))
        else:
            form = forms.NewTodoForm(initial={"category": kwargs.get("category_id")})

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


class TaskCategoryCreateFormHTMXView(FormView):
    # TODO: Todo should be able to return whole new card
    def get(self, request, *args, **kwargs):
        if "todo_category_id" in kwargs:
            print("Got an id yay")
            form = forms.NewTodoCategoryForm(instance=models.TodoCategory.objects.get(id=kwargs["todo_category_id"]))
        else:
            form = forms.NewTodoCategoryForm()

        return render(
            request,
            "components/todos/card_todo_card_blank_create.html",
            context={"form": form, "todo_category_id": kwargs.get("todo_category_id")}
        )

    def post(self, request, *args, **kwargs):
        if "todo_category_id" in kwargs:
            form = forms.NewTodoCategoryForm(request.POST, instance=models.TodoCategory.objects.get(id=kwargs["todo_category_id"]))
        else:
            form = forms.NewTodoCategoryForm(request.POST)
        todo_category = form.save()

        return render(
            request,
            "components/todos/card_todo_header.html",
            context={"category": todo_category}
        )


def htmx_complete_todo(request, todo_id):

    todo = models.Todo.objects.get(id=todo_id)
    todo.complete_time = datetime.datetime.now()
    todo.save()

    response = HttpResponse(status=203)
    response["HX-Trigger"] = "refreshCountToday"
    return response


class TaskRetrieveHTMXView(HTMXTemplateMixin, TemplateView):

    def get_context_data(self, **kwargs):
        return {"todo": models.Todo.objects.get(id=self.kwargs["todo_id"])}


class TaskCategoryRetrieveHTMXView(HTMXTemplateMixin, TemplateView):

    def get_context_data(self, **kwargs):
        return {"category": models.TodoCategory.objects.get(id=self.kwargs["todo_category_id"])}


class DiaryCreateFormHTMXView(FormView):

    def get(self, request, *args, **kwargs):

        if "pk" in kwargs:
            diary_entry = models.DiaryEntry.objects.get(id=kwargs["pk"])
            form = forms.DiaryEntryForm(instance=diary_entry)
        else:
            diary_entry = models.DiaryEntry.objects.get_or_create(date=datetime.date.today(), category__isnull=True)
            form = forms.DiaryEntryForm(initial={"text": kwargs["pk"]})

        return render(
            request,
            "components/diary/diary_form.html",
            context={"form": form, "inline_form": True, "entry": diary_entry}
        )

    def post(self, request, *args, **kwargs):

        if "pk" in kwargs:
            diary_entry = models.DiaryEntry.objects.get(
                id=kwargs["pk"], category__isnull=True)
        else:
            diary_entry, _ = models.DiaryEntry.objects.get_or_create(date=datetime.date.today(), category__isnull=True)

        form = forms.DiaryEntryForm(request.POST, instance=diary_entry)
        form.save()
        return render(
            request,
            "components/diary/diary_entry.html",
            context={"entry": diary_entry})


def htmx_delete_todo_category_view(request, pk):
    """Soft-delete a todo category"""
    category = models.TodoCategory.objects.get(pk=pk)
    category.deactivate_time = datetime.datetime.now()
    category.save()
    return HttpResponse(status=203)


def htmx_delete_element(request):
    """Return nothing so the frontend can delete the element"""
    return HttpResponse(status=203)
