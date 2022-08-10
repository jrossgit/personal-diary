from django.forms import ModelForm
from app import models


class NewTodoForm(ModelForm):
    class Meta:
        model = models.Todos
        fields = ["category", "text"]


class NewTodoCategoryForm(ModelForm):
    class Meta:
        model = models.TodoCategory
        fields = ["name"]
