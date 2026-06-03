# from django.http import HttpResponse
import os

from django.shortcuts import render
from littlelemon.settings import STATIC_URL

from .forms import BookingForm
from .models import MenuItem


def home(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def book(request):
    form = BookingForm()
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {"form": form}
    return render(request, "book.html", context)


# Add your code here to create new views
def menu(request):
    menu_data = MenuItem.objects.filter(featured=True)
    main_data = {"menu": menu_data}
    return render(request, "menu.html", main_data)


def display_menu_item(request, pk=None):
    # default menu item response
    menu_item = ""
    menu_item_data = {"menu_item": menu_item}
    if pk:
        # pull menu item
        menu_item = MenuItem.objects.get(pk=pk)
        # generate image file path
        menu_item.image_filepath = f"/{STATIC_URL}img/menu_items/{menu_item.name}.jpg"
        # check if image file exists
        if os.path.exists(os.path.abspath(f".{menu_item.image_filepath}")):
            menu_item_data = {"menu_item": menu_item}
    return render(request, "menu_item.html", menu_item_data)
