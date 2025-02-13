from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)  # 类别名称
    views = models.IntegerField(default=0)  # 访问次数
    likes = models.IntegerField(default=0)  # 点赞次数

    class Meta:
        verbose_name_plural = "Categories"
    def __str__(self):
        return self.name  # 让 Django 在管理界面显示名称

class Page(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # 外键关联类别
    title = models.CharField(max_length=128)  # 页面标题
    url = models.URLField()  # 页面链接
    views = models.IntegerField(default=0)  # 访问次数


    def __str__(self):
        return self.title  # 让 Django 在管理界面显示标题