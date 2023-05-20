import datetime

from django.shortcuts import HttpResponse, render

from app.forms import DiaryEntryForm
from app.models import DiaryEntry, TodoCategory, Todo


