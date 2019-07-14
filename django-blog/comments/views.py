from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post

from .models import Comment
from .forms import CommentForm


def post_comment(request, post_pk):
    # 先获取被评论的文章存在时，则获取；否则返回 404 页面给用户。
    post = get_object_or_404(Post, pk=post_pk)

    # 因此只有当用户的请求为 post 时才需要处理表单数据。
    if request.method == 'POST':
        # 提交的数据存在 request.POST 中，是一个类字典对象。
        form = CommentForm(request.POST)

        # 当调用 form.is_valid() 方法时，Django 自动检查表单的数据是否符合格式要求。
        if form.is_valid():
            # 调用表单的 save 方法保存数据到数据库，
            # commit=False 利用表单的数据生成 Comment 模型类的实例
            comment = form.save(commit=False)
            # 将评论和被评论的文章关联起来。
            comment.post = post
            # 将评论数据保存进数据库，调用模型实例的 save 方法
            comment.save()
            # 重定向到 post 的详情页，当 redirect 函数接收一个模型的实例时，会调用这个模型实例的 get_absolute_url 方法，
            # 然后重定向到 get_absolute_url 方法返回的 URL。
            return redirect(post)

        else:
            # 检查到数据不合法，重新渲染详情页，并且渲染表单的错误。
            comment_list = post.comment_set.all()
            context = {'post': post,
                       'form': form,
                       'comment_list': comment_list
                       }
            return render(request, 'blog/detail.html', context=context)
    # 不是 post 请求，说明用户没有提交数据，重定向到文章详情页。
    return redirect(post)
