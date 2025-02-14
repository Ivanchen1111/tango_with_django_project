from django.shortcuts import render, get_object_or_404, redirect
from rango.forms import CategoryForm, PageForm
from rango.models import Category, Page
from django.urls import reverse
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime


def index(request):
    visits = request.session.get('visits', 0) + 1
    request.session['visits'] = visits
    request.session.set_expiry(3600)  # 让 session 在 1 小时后过期

    visitor_cookie_handler(request)
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {
        'categories': category_list,
        'pages': page_list,
        'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!',
        'visits': visits  # 确保传递 `visits`
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



@login_required
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



@login_required
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


def register(request):
    registered = False  # 默认用户未注册

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()  # 保存用户
            user.set_password(user.password)  # 加密密码
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user  # 关联 UserProfile 和 User
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)  # 打印错误信息

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered
    })



def user_login(request):
    # 处理用户提交的登录信息
    if request.method == 'POST':
        username = request.POST.get('username')  # 获取用户名
        password = request.POST.get('password')  # 获取密码

        # 使用 Django 内置方法验证用户名和密码
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:  # 检查用户是否是激活状态
                login(request, user)  # 登录用户
                return redirect(reverse('rango:index'))  # 跳转到首页
            else:
                return HttpResponse("Your Rango account is disabled.")  # 账号被禁用
        else:
            print(f"Invalid login details: {username}, {password}")  # 记录错误信息
            return HttpResponse("Invalid login details supplied.")  # 登录失败提示

    # 处理 GET 请求，返回登录页面
    return render(request, 'rango/login.html')


@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")



# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('rango:index'))

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')


def set_cookie(request):
    response = HttpResponse("Cookie has been set!")
    response.set_cookie('visits', 1, max_age=3600)
    return response


def get_cookie(request):
    visits = request.COOKIES.get('visits', 'No cookie found')
    return HttpResponse(f"Visits: {visits}")

def update_cookie(request):
    visits = int(request.COOKIES.get('visits', 0)) + 1  # 读取 visits 并加 1
    response = HttpResponse(f"Updated visits: {visits}")
    response.set_cookie('visits', visits, max_age=3600)  # 重新设置 cookie
    return response

def delete_cookie(request):
    response = HttpResponse("Cookie deleted!")
    response.delete_cookie('visits')
    return response

def set_session_view(request):
    request.session['username'] = 'IvanChen'
    request.session['favorite_color'] = 'Blue'
    return HttpResponse("Session has been set!")


def get_session_view(request):
    username = request.session.get('username', 'Guest')
    favorite_color = request.session.get('favorite_color', 'No favorite color set.')
    return HttpResponse(f"Username: {username}, Favorite Color: {favorite_color}")


def delete_session_view(request):
    request.session.flush()
    return HttpResponse("Session has been deleted!")

def visitor_cookie_handler(request):
    """ Handles session-based visit tracking """
    visits = int(request.session.get('visits', 1))
    last_visit_cookie = request.session.get('last_visit', str(datetime.now()))

    last_visit_time = datetime.strptime(last_visit_cookie, "%Y-%m-%d %H:%M:%S.%f")

    # If more than 5 seconds have passed since the last visit, increment visits
    if (datetime.now() - last_visit_time).seconds > 5:
        visits += 1
        request.session['last_visit'] = str(datetime.now())  # Update last_visit timestamp
    else:
        request.session['last_visit'] = last_visit_cookie  # Keep the previous timestamp

    request.session['visits'] = visits  # Store the updated visit count
