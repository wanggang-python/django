import markdown

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible
from django.utils.html import strip_tags


# 装饰器用于兼容 Python2
@python_2_unicode_compatible
class Category(models.Model):
    """分类"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Tag(models.Model):
    """标签"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Post(models.Model):
    """ 文章 """
    # 文章标题
    title = models.CharField(max_length=70)
    # 存储比较短的字符串可以使用 CharField，但对于文章的正文来说可能会是一大段文本，因此使用 TextField 来存储大段文本。
    body = models.TextField()
    # 创建时间和最后一次修改时间，存储时间的字段用 DateTimeField 类型。
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    # 文章摘要，可以没有文章摘要，但默认情况下 CharField 要求我们必须存入数据，否则就会报错。
    # 指定 CharField 的 blank=True 参数值后就可以允许空值了。
    excerpt = models.CharField(max_length=200, blank=True)
    # views 字段记录阅读量
    views = models.PositiveIntegerField(default=0)
    # 一篇文章只能对应一个分类，但是一个分类下可以有多篇文章，所以用的是 ForeignKey，一对多的关联关系。
    category = models.ForeignKey(Category)
    #一篇文章可以有多个标签，同一个标签下也可能有多篇文章，所以用 ManyToManyField，多对多的关联关系。
    # 文章可以没有标签，因此为标签 tags 指定了 blank=True。
    tags = models.ManyToManyField(Tag, blank=True)
    # django.contrib.auth 是 Django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是 Django 为我们已经写好的用户模型。
    # 这里我们通过 ForeignKey 把文章和 User 关联了起来。
    # 因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，一对多的关联关系
    author = models.ForeignKey(User)

    def __str__(self):
        return self.title

    # 自定义 get_absolute_url 方法
    # 'blog:detail'blog 应用下的 name=detail 的函数,返回当前自己的 URL
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})
    # 指定 Post 的排序方式,ordering 属性用来指定文章排序方式按时间降序
    class Meta:
        ordering = ['-created_time']
    # increase_views 方法将自身对应的 views 字段的值 +1    
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        # 如果没有填写摘要
        if not self.excerpt:
            # 实例化一个 Markdown 类，用于渲染 body 的文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 先将 Markdown 文本渲染成 HTML 文本
            # strip_tags 去掉 HTML 文本的全部 HTML 标签从文本摘取前 54 个字符赋给 excerpt
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        # 调用父类的 save 方法将数据保存到数据库中
        super(Post, self).save(*args, **kwargs)
