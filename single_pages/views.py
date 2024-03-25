from django.shortcuts import render
from shop.models import Yarn, Category, Manufacturer

# Create your views here.
def home(request) :
    recent_updates = Yarn.objects.order_by('-pk')[:3]
    return render(request, 'single_pages/home.html',
                  {'recent_updates' : recent_updates})

def my_page(request) :
    return render(request, 'single_pages/my_page.html')

def introduction(request) :
    return render(request, 'single_pages/introduction.html', {
        'categories' : Category.objects.all(),
        'manufacturers' : Manufacturer.objects.all()
    })