import uuid

from django.db import models


# TODO Rename this as `Todo`
class Todos(models.Model):

    class Meta:
        ordering = ["-create_time"]

    def __str__(self):
        return self.text

    id = models.fields.UUIDField(verbose_name="Todo UUID", primary_key=True, default=uuid.uuid4)
    text = models.fields.CharField(verbose_name="What to do?", max_length=256)
    create_time = models.DateTimeField(verbose_name="Time todo created", auto_now_add=True)
    complete_time = models.DateTimeField(verbose_name="Time todo completed", null=True, blank=True)

    category = models.ForeignKey("TodoCategory", on_delete=models.CASCADE, null=True, blank=True)


class TodoCategory(models.Model):

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    id = models.fields.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.fields.CharField(max_length=256)
    create_time = models.DateTimeField(verbose_name="Time todo created", auto_now_add=True)
    deactivate_time = models.DateTimeField(verbose_name="Time todo completed", null=True, blank=True)


# class Diary(models.Model):

#     id = models.fields.UUIDField(verbose_name="Todo UUID", primary_key=True, default=uuid.uuid4)
#     name = models.fields.CharField(max_length=128)
#     # Auto slug field
#     end_date = models.fields.DateField()

# class DiaryEntry(models.Model):

#     id = models.fields.UUIDField(verbose_name="Todo UUID", primary_key=True, default=uuid.uuid4)
#     text = models.fields.TextField()
#     date = models.fields.DateField(auto_now=)
#     diary = models.fields.