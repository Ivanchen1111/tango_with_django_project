from django.test import TestCase
from rango.models import Category, Page

class Chapter5Tests(TestCase):
    def setUp(self):
        """创建测试数据"""
        self.category = Category.objects.create(name='Test Category', views=10, likes=5)
        self.page = Page.objects.create(category=self.category, title='Test Page', url='http://example.com', views=20)

    def test_category_creation(self):
        """测试 Category 模型是否正确创建"""
        self.assertEqual(self.category.name, 'Test Category')
        self.assertEqual(self.category.views, 10)
        self.assertEqual(self.category.likes, 5)

    def test_page_creation(self):
        """测试 Page 模型是否正确创建"""
        self.assertEqual(self.page.title, 'Test Page')
        self.assertEqual(self.page.url, 'http://example.com')
        self.assertEqual(self.page.views, 20)
        self.assertEqual(self.page.category.name, 'Test Category')

    def test_category_str(self):
        """测试 Category 的 __str__ 方法"""
        self.assertEqual(str(self.category), 'Test Category')

    def test_page_str(self):
        """测试 Page 的 __str__ 方法"""
        self.assertEqual(str(self.page), 'Test Page')

    def test_admin_list_display(self):
        """测试 Django Admin 界面是否正确显示 Page 信息"""
        from rango.admin import PageAdmin
        page_admin = PageAdmin(Page, None)
        self.assertEqual(page_admin.list_display, ('title', 'category', 'url'))

