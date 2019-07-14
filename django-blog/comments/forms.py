# Django 的表单类必须继承自 forms.Form 类或者 forms.ModelForm 类
from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # 需要显示的字段
        fields = ['name', 'email', 'url', 'text']
