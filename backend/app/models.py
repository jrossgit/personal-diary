from datetime import date
import uuid

from django.db import models
from django.utils.text import slugify


class TodoManager(models.Manager):

    def completed_on_date(self, date):
        return self.filter(complete_time__date=date)

    def completed_today(self):
        return self.completed_on_date(date.today())


class Todo(models.Model):

    objects = TodoManager()

    class Meta:
        ordering = ["-create_time"]

    def __str__(self):
        return self.text

    id = models.fields.UUIDField(verbose_name="Todo UUID", primary_key=True, default=uuid.uuid4)
    text = models.fields.CharField(verbose_name="", max_length=256)
    create_time = models.DateTimeField(verbose_name="Time todo created", auto_now_add=True)
    complete_time = models.DateTimeField(verbose_name="Time todo completed", null=True, blank=True)

    category = models.ForeignKey("TodoCategory", on_delete=models.CASCADE, null=True, blank=True, related_name="todos")


class TodoCategory(models.Model):

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    id = models.fields.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.fields.CharField(max_length=256)
    create_time = models.DateTimeField(verbose_name="Time todo created", auto_now_add=True)
    deactivate_time = models.DateTimeField(verbose_name="Time todo completed", null=True, blank=True)

    @property
    def card_slug(self):
        if self.name:
            return f"category-{slugify(self.name)}"


class DiaryEntry(models.Model):

    def __str__(self):
        if self.category:
            return f"Diary {self.date} ({self.category.name})"
        else:
            return f"Diary {self.date}"

    id = models.fields.UUIDField(verbose_name="Todo UUID", primary_key=True, default=uuid.uuid4)
    text = models.fields.TextField()
    date = models.fields.DateField(auto_now_add=True)
    category = models.ForeignKey("TodoCategory", on_delete=models.CASCADE, null=True, blank=True, related_name="diary_entries")
