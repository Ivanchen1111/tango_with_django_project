from django.test import TestCase
from django.urls import reverse
from rango.models import Category, Page
from django.contrib.auth.models import User

class Chapter7Tests(TestCase):
    def setUp(self):
        """测试开始前，创建一些测试数据"""
        self.category = Category.objects.create(name="Python", views=10, likes=5, slug="python")
        self.page = Page.objects.create(category=self.category, title="Django Rocks", url="http://www.djangoproject.com")

    def test_index_view(self):
        """测试 index 主页是否能正确访问"""
        response = self.client.get(reverse('rango:index'))  # 确保使用 'rango:index'
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rango/index.html')

    def test_category_view(self):
        """测试 category 视图是否能正确访问"""
        response = self.client.get(reverse('rango:show_category', args=['python']))  # 确保使用 'rango:show_category'
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rango/category.html')

    def test_add_page_view(self):
        """测试 add_page 视图是否能正确访问"""
        response = self.client.get(reverse('rango:add_page', args=['python']))  # 确保使用 'rango:add_page'
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rango/add_page.html')


    def test_reverse_urls(self):
        """测试 Django 反向解析 URL 是否成功"""
        self.assertEqual(reverse('rango:index'), '/')  # 确保解析 '/' 而不是 '/rango/'
        self.assertEqual(reverse('rango:show_category', args=['python']), '/category/python/')
        self.assertEqual(reverse('rango:add_page', args=['python']), '/category/python/add_page/')
