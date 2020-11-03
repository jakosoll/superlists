from django.shortcuts import render, redirect
from .models import Item, List

# Create your views here.


def home_page(request):
    """home page"""
    return render(request, 'home.html')


def view_list(request, pk):
    """представление списка"""
    list_ = List.objects.get(id=pk)
    return render(request, 'list.html', {'list': list_})


def new_list(request):
    """новый список"""
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')


def add_item(request, pk):
    """Добавить новый элемент"""
    list_ = List.objects.get(id=pk)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')

