from django.shortcuts import render, redirect

from app import forms, models


def home_view(request):
    return "Hello!"
