from django.shortcuts import render
from rango.models import Category, Page

def index(request):
    category_list = Category.objects.all()
    page_list = Page.objects.all()
    context_dict = {'categories': category_list, 'pages': page_list}
    return render(request, 'rango/index.html', context_dict)

def about(request):
    return render(request, 'rango/about.html')
