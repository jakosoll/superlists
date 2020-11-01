from django.shortcuts import render, redirect
from .models import Item, List

# Create your views here.


def home_page(request):
    """home page"""
    return render(request, 'home.html')


def view_list(request, pk):
    """представление списка"""
    list_ = List.objects.get(id=pk)
    items = Item.objects.filter(list=list_)
    return render(request, 'list.html', {'items': items})


def new_list(request):
    """новый список"""
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')
