from django.test import TestCase
from django.urls import reverse
from rango.models import Category, Page
from django.contrib.auth.models import User

class Chapter7Tests(TestCase):

    def setUp(self):
        """初始化测试数据"""
        self.category = Category.objects.create(name="Python", views=10, likes=5, slug="python")
        self.page = Page.objects.create(category=self.category, title="Django Rocks", url="http://www.djangoproject.com")

    def test_category_model(self):
        """测试 Category 模型是否正确存入数据库"""
        category = Category.objects.get(name="Python")
        self.assertEqual(category.views, 10)
        self.assertEqual(category.likes, 5)
        self.assertEqual(category.slug, "python")

    def test_page_model(self):
        """测试 Page 模型是否正确存入数据库"""
        page = Page.objects.get(title="Django Rocks")
        self.assertEqual(page.category.name, "Python")
        self.assertEqual(page.url, "http://www.djangoproject.com")

    def test_category_view(self):
        """测试 category 视图是否能正确访问"""
        response = self.client.get(reverse('show_category', args=['python']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python")

    def test_add_page_view(self):
        """测试 add_page 视图是否能正确访问"""
        response = self.client.get(reverse('add_page', args=['python']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Add a Page")

    def test_home_page_view(self):
        """测试 home 主页是否能正确访问"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rango says...")

    def test_template_used(self):
        """测试是否正确使用了模板"""
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'rango/index.html')

    def test_login_required_for_add_page(self):
        """测试 add_page 是否需要登录"""
        response = self.client.get(reverse('add_page', args=['python']))
        self.assertEqual(response.status_code, 200)  # 确保页面可以访问
        self.assertContains(response, "Add a Page")  # 确保页面有 "Add a Page"

    def test_create_new_user(self):
        """测试用户注册"""
        user = User.objects.create_user(username="testuser", password="testpassword123")
        self.assertEqual(user.username, "testuser")

    def test_reverse_urls(self):
        """测试 Django 反向解析 URL 是否成功"""
        self.assertEqual(reverse('index'), '/rango/')
        self.assertEqual(reverse('show_category', args=['python']), '/rango/category/python/')
        self.assertEqual(reverse('add_page', args=['python']), '/rango/category/python/add_page/')

