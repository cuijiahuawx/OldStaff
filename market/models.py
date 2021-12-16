from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):
    用户 = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    昵称 = models.CharField(max_length=200, null=True, blank=True, default="未命名")
    手机 = models.CharField(max_length=200, null=True, blank=True)
    QQ = models.CharField(max_length=200, null=True, blank=True)
    地址 = models.CharField(max_length=200, null=True, blank=True)
    头像 = models.ImageField(null=True, blank=True)

    class Meta:
        verbose_name_plural = '用户信息'
    def __str__(self):
        return self.用户.username

class Catgory(models.Model):
    分类 = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name_plural = '分类'
    def __str__(self):
        return self.分类

class Good(models.Model):
    发布人 = models.ForeignKey(Customer, on_delete=models.CASCADE)
    分类 = models.ManyToManyField(Catgory)
    图片 = models.ImageField()
    名称 = models.CharField(max_length=200)
    简介 = models.TextField(null=True, blank=True)
    价格 = models.IntegerField(null=True, blank=True)
    时间 = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id'] 
        verbose_name_plural = '商品'
    def __str__(self):
        return self.名称
    
class Collect(models.Model):
    收藏人 = models.ForeignKey(Customer, on_delete=models.CASCADE)
    商品 = models.ForeignKey(Good, on_delete=models.CASCADE)
    创建时间 = models.TimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id'] 
        verbose_name_plural = '收藏'
    def __str__(self):
        return self.收藏人.昵称 + ',' + self.商品.名称