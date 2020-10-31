from django.shortcuts import render, redirect
from .models import Item

# Create your views here.


def home_page(request):
    """home page"""
    if request.method == 'POST':
        new_item_text = request.POST['item_text']
        Item.objects.create(text=new_item_text)
        return redirect('/')
    return render(request, 'home.html')
