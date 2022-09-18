import datetime

from django import forms
from app import models


class NewTodoForm(forms.ModelForm):
    class Meta:
        model = models.Todos
        fields = ["category", "text"]


class NewTodoCategoryForm(forms.ModelForm):
    class Meta:
        model = models.TodoCategory
        fields = ["name"]


class DiaryEntryForm(forms.ModelForm):

    text = forms.CharField(label="Diary", widget=forms.Textarea)

    class Meta:
        model = models.DiaryEntry
        fields = ["text"]
