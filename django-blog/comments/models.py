from django.db import models
from django.utils.six import python_2_unicode_compatible


# python_2_unicode_compatible 装饰器用于兼容 Python2
@python_2_unicode_compatible
class Comment(models.Model):
	# 用户名
    name = models.CharField(max_length=100)
    # 邮箱
    email = models.EmailField(max_length=255)
    # 个人网站
    url = models.URLField(blank=True)
    # 发表的内容
    text = models.TextField()
    # 记录评论时间auto_now_add自动把值指定为当前时间
    created_time = models.DateTimeField(auto_now_add=True)
    # 设置主键关联到某篇文章
    post = models.ForeignKey('blog.Post')
    def __str__(self):
        return self.text[:20]
