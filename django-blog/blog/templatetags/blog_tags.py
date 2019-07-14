from django import template
from django.db.models.aggregates import Count

from ..models import Post, Category, Tag


#注册模板标签,返回
register = template.Library()

# 最新文章模板标签获取数据库中前 5 篇文章
@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all()[:num]

# 归档模板标签,按月归档
@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')

# 分类模板标签
@register.simple_tag
def get_categories():
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)

@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
