from django.contrib import admin
from .models import Post, Category, Tag

# 自定义admin后台视图,增加标题,创建时间和修改时间,分类和作者
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']

#注册创建的模型 
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
