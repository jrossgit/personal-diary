import datetime

from django.db.models import Prefetch
from django.shortcuts import render, redirect, reverse

from app import forms, models


def home_view(request):
    unsorted_todos = models.Todo.objects.filter(
        complete_time__isnull=True,
        category__isnull=True)
    sorted_todos = models.Todo.objects.filter(
        complete_time__isnull=True,
        category__isnull=False
    ).order_by("category__name")

    categories = models.TodoCategory.objects.filter(
        deactivate_time__isnull=True
    ).prefetch_related(
        Prefetch(
            "todos",
            queryset=models.Todo.objects.filter(
                complete_time__isnull=True,
                category__isnull=False
            )
        )
    )

    return render(request, template_name="home.html", context={
        "sorted_todos": sorted_todos,
        "unsorted_todos": unsorted_todos,
        "new_categories": categories,
        "form": forms.NewTodoForm(),
    })


def create_todo(request, category_id=None):
    if request.method == "GET":

        new_todo_form = forms.NewTodoForm(initial={"category": category_id})
        return render(request, template_name="create_todo.html", context={
            "form": new_todo_form,
        })
    elif request.method == "POST":
        form = forms.NewTodoForm(request.POST)
        todo = form.save()
        redirect_slug = f"#{todo.category.card_slug}" if todo.category else ""
        return redirect(f"{reverse('home')}{redirect_slug}")


def create_todo_category(request):
    if request.method == "GET":
        return render(request, template_name="create_todo_category.html", context={
            "form": forms.NewTodoCategoryForm(),
        })
    elif request.method == "POST":
        form = forms.NewTodoCategoryForm(request.POST)
        form.save()
        return redirect("home")


def create_update_diary_entry(request, entry_id=None):

    if entry_id:
        diary_entry = models.DiaryEntry.objects.get(
            id=entry_id, category__isnull=True)
    else:
        diary_entry, _ = models.DiaryEntry.objects.get_or_create(date=datetime.date.today(), category__isnull=True)

    if request.method == "GET":
        form = forms.DiaryEntryForm(instance=diary_entry)
        recent_entries = models.DiaryEntry.objects.filter(
            date__lte=datetime.date.today() - datetime.timedelta(days=1),
            date__gte=datetime.date.today() - datetime.timedelta(days=14),
            category__isnull=True
        ).order_by("-date")

        return render(request, template_name="create_diary_entry.html", context={
            "entry": diary_entry,
            "form": form,
            "today": datetime.date.today(),
            "recent_entries": recent_entries,
        })

    elif request.method == "POST":
        form = forms.DiaryEntryForm(request.POST, instance=diary_entry)
        form.save()
        return redirect("diary-create-update")
