from django.shortcuts import render, get_object_or_404, redirect
from rango.forms import CategoryForm, PageForm  # 确保引入 PageForm
from rango.models import Category, Page
from django.urls import reverse


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

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.views = 0
            category.likes = 0
            category.save()
            return redirect(reverse('rango:index'))  # 使用 reverse 代替硬编码 URL
        else:
            print(form.errors)
    else:
        form = CategoryForm()

    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):
    category = get_object_or_404(Category, slug=category_name_slug)

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            page = form.save(commit=False)
            page.category = category  # 关联到正确的 category
            page.save()
            return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category.slug}))
        else:
            print(form.errors)
    else:
        form = PageForm()

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)
