from rest_framework.decorators import api_view
from rest_framework.response import Response

from app import models


@api_view(http_method_names=["POST"])
def create_brainworm_todo(request):
    if request.method == "POST":
        brainworms_cat, _ = models.TodoCategory.objects.get_or_create(name="Brainworms")
        print(brainworms_cat)
        models.Todo.objects.create(category=brainworms_cat, text=request.data["text"])
    return Response({"message": "Successful"})
