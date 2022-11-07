from django.shortcuts import render
import os


def home_page(request):
    return render(request, 'home.html', {'new_item_text': request.POST.get('item_text', ''), })
# Create your views here.
