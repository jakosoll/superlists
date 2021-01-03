from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from .models import Item, List

# Create your views here.


def home_page(request):
    """home page"""
    return render(request, 'home.html')


def view_list(request, pk):
    """представление списка"""
    list_ = List.objects.get(id=pk)
    if request.method == "POST":
        Item.objects.create(text=request.POST['item_text'], list=list_)
        return redirect(f'/lists/{list_.id}/')
    return render(request, 'list.html', {'list': list_})


def new_list(request):
    """новый список"""
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {"error": error})
    return redirect(f'/lists/{list_.id}/')

# TODO: Удалеть захардкоженные URL-адреса в представлении

