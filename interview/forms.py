# _*_ coding: utf-8 _*_
from django import forms

class RegForm(forms.Form):
    """
    用户注册表单
    """
    # 必填项,并且最大用户名长度为20个字符
    # username = forms.CharField(required=True, max_length=100,error_messages={"required": "用户名不能为空"})
    email = forms.EmailField(required=True, max_length=100, error_messages={"required": "邮箱不能为空"})
    # 必填项,并且最小密码长度为8个字符
    password = forms.CharField(required=True, min_length=8, error_messages={"required": "密码长度不能小于8位"})

class LoginForm(forms.Form):
    """
    用户登录表单
    """
    email = forms.EmailField(required=True, max_length=100, error_messages={"required": "邮箱不能为空"})
    password = forms.CharField(required=True, min_length=8, error_messages={"required": "密码长度不能小于8位"})

class CommentForm(forms.Form):
    """
    用户评论表单
    """
    comment = forms.CharField(required=True,max_length=100,error_messages={"require":"内容不能为空"})