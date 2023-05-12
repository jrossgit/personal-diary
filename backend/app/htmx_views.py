import datetime

from django.shortcuts import HttpResponse, render
from django.forms import HiddenInput

from app.forms import DiaryEntryForm, NewTodoForm
from app.models import DiaryEntry, TodoCategory, Todo


# def create_todo_htmx_form(request, category_id=None, todo_id=None):

#     if request.method == "GET":
#         if todo_id:
#             form = NewTodoForm(instance=Todo.objects.get(id=todo_id))
#         else:
#             form = NewTodoForm(initial={"category": category_id})

#         form.fields["category"].widget = HiddenInput()

#         print(f"rendering with {form} and {todo_id}")
#         return render(
#             request,
#             "components/todos/card_todo_create.html",
#             context={"form": form, "todo_id": todo_id}
#         )

#     elif request.method == "POST":
#         if todo_id:
#             form = NewTodoForm(request.POST, instance=Todo.objects.get(id=todo_id))
#         else:
#             form = NewTodoForm(request.POST)
#         todo = form.save()
#         return render(
#             request,
#             "components/todos/card_todo.html",
#             context={"todo": todo})


def delete_element(request):
    """Return nothing so the frontend can delete the element"""
    return HttpResponse(status=203)


def todo_htmx(request, todo_id):
    """Fetch the todo row for a card"""
    todo = Todo.objects.get(id=todo_id)
    return render(
        request,
        "components/todos/card_todo.html",
        context={"todo": todo})


def complete_todo(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    if not todo.complete_time:
        todo.complete_time = datetime.datetime.now()
        todo.save()

    response = HttpResponse(status=203)
    response["HX-Trigger"] = "refreshCountToday"
    return response


def create_diary_entry_htmx_form(request, diary_entry_id=None):

    if diary_entry_id:
        diary_entry = DiaryEntry.objects.get(
            id=diary_entry_id, category__isnull=True)
    else:
        diary_entry, _ = DiaryEntry.objects.get_or_create(date=datetime.date.today(), category__isnull=True)

    if request.method == "GET":
        if diary_entry_id:
            form = DiaryEntryForm(instance=DiaryEntry.objects.get(id=diary_entry_id))
        else:
            form = DiaryEntryForm(initial={"text": diary_entry_id})

        return render(
            request,
            "components/diary/diary_form.html",
            context={"form": form, "inline_form": True, "entry": diary_entry}
        )

    elif request.method == "POST":
        form = DiaryEntryForm(request.POST, instance=diary_entry)
        form.save()
        return render(
            request,
            "components/diary/diary_entry.html",
            context={"entry": diary_entry})


def delete_todo_category(request, id):

    category = TodoCategory.objects.get(id=id)
    category.deactivate_time = datetime.datetime.now()
    category.save()
    return HttpResponse(status=203)
