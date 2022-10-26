from django.shortcuts import render
import os


def home_page(request):
    return render(request, 'home.html')
# Create your views here.
