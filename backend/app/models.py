import uuid

from django.db import models


# Create your models here.
class Todos(models.Model):

    class Meta:
        ordering = ["-create_time"]

    def __str__(self):
        return f"Todo [{'X' if self.completed_at else ''}] <{self.text}>"

    id = models.fields.UUIDField(verbose_name="Todo UUID", primary_key=True, default=uuid.uuid4)
    text = models.fields.CharField(verbose_name="What to do?", max_length=256)
    create_time = models.DateTimeField(verbose_name="Time todo created", auto_now_add=True)
    complete_time = models.DateTimeField(verbose_name="Time todo completed", null=True, blank=True)
