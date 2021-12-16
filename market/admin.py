from django.contrib import admin
from .models import *


class GoodAdmin(admin.ModelAdmin):
    list_display=('id', '发布人', '分类显示', '图片', '名称', '简介', '价格', '时间')
    
    def 分类显示(self, obj):
        return [i.分类 for i in obj.分类.all()]
    filter_horizontal  =  ("分类", )
class CustomerAdmin(admin.ModelAdmin):
    list_display=('id','用户','昵称','手机','QQ','地址','头像')

class CatgoryAdmin(admin.ModelAdmin):
    list_display=('id','分类')

class CollectAdmin(admin.ModelAdmin):
    list_display=('id','收藏人','商品')


admin.site.register(Good, GoodAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Catgory, CatgoryAdmin)
admin.site.register(Collect, CollectAdmin)