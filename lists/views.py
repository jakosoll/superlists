from django.shortcuts import render, redirect
from .models import Item

# Create your views here.


def home_page(request):
    """home page"""
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/one-in-whole-world-list/')
    return render(request, 'home.html')


def view_list(request):
    """представление списка"""
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})
