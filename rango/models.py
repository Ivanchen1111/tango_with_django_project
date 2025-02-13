from django.db import models
from django.utils.text import slugify

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)  # 类别名称
    slug = models.SlugField(unique=True, default="", blank=True)
    views = models.IntegerField(default=0)  # 访问次数
    likes = models.IntegerField(default=0)  # 点赞次数

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

            # 确保 slug 唯一
            original_slug = self.slug
            counter = 1
            while Category.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super(Category, self).save(*args, **kwargs)

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