from django.shortcuts import render, get_object_or_404
from rango.models import Category, Page

def index(request):
    # 获取点赞最多的 5 个 Category（按 likes 降序排序）
    category_list = Category.objects.order_by('-likes')[:5]

    # 获取访问量最多的 5 个 Page（按 views 降序排序）
    page_list = Page.objects.order_by('-views')[:5]

    # 传递数据给模板
    context_dict = {
        'categories': category_list,
        'pages': page_list,
        'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'
    }

    return render(request, 'rango/index.html', context_dict)

def about(request):
    return render(request, 'rango/about.html')

def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['category'] = category
        context_dict['pages'] = pages
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context=context_dict)

