from rest_framework.decorators import api_view
from rest_framework.response import Response

from app import models


@api_view(http_method_names=["GET"])
def list_todo_categories(request):
    if request.method == "GET":
        categories = models.TodoCategory.objects.filter(deactivate_time__isnull=True)
    return Response({"todo_categories": [
        {"id": c.id, "name": c.name} for c in categories
    ]})


@api_view(http_method_names=["POST"])
def create_todo(request, category_id):
    if request.method == "POST":
        category = models.TodoCategory.objects.get(id=category_id)
        models.Todo.objects.create(category=category, text=request.data["text"])
    return Response({"message": "Successful"})
