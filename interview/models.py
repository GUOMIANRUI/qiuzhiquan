# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from datetime import datetime

from django.db import models   # 从内置的模块导入
from django.contrib.auth.models import AbstractUser
from DjangoUeditor.models import UEditorField

# Create your models here.

class User(AbstractUser):
    """
    用户表
    """
    # username = models.CharField(verbose_name="姓名",max_length=50)
    # email = models.CharField(verbose_name="邮箱",max_length=50)
    # password = models.CharField(verbose_name="密码",max_length=128)
    mobile = models.CharField(verbose_name="手机",max_length=11,blank=True,null=True)
    birthday = models.DateField(verbose_name="生日",blank=True,null=True)
    gen = (
        ("male","男"),
        ("female","女")
    )
    gender = models.CharField(verbose_name="性别",choices=gen,default="male",max_length = 10)
    image = models.ImageField(verbose_name="头像",upload_to="users/%Y/%m",blank=True,null=True)

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.username   # unicode重载  使后台中文显示

class Author(models.Model):
    """
    作者表
    """
    name = models.CharField(verbose_name="姓名",max_length=50)
    desc = models.TextField(verbose_name="简介",max_length=500)
    profession = models.CharField(verbose_name="专业",max_length=50)
    years = (
        ("1","2020届"),
        ("2","2019届"),
        ("3","2018届"),
        ("4","2017届"),
    )
    year = models.CharField(verbose_name="年级",choices=years,default="1",max_length=60)

    class Meta:
        verbose_name = "作者"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.name

class Interview(models.Model):
    title = models.CharField(verbose_name="标题",max_length=50)
    desc = models.CharField(verbose_name="描述",max_length=100)
    # content = models.TextField(verbose_name="内容",max_length=5000)
    content = UEditorField(verbose_name="内容", width=700, height=200, default="",
                           imagePath="content/%(basename)s_%(datetime)s.%(extname)s",
                           filePath="content/%(basename)s_%(datetime)s.%(extname)s")
    image = models.ImageField(verbose_name="封面",upload_to="interview/%Y/%m")
    author = models.ForeignKey(Author,verbose_name="所属作者")  # 外键
    company = models.CharField(verbose_name="公司",max_length=50)
    trades = (
        ("t1","互联网"),
        ("t2","网络安全"),
        ("t3","运营商"),
        ("t4","银行"),
        ("t5","集成商"),
        ("t6","国企"),
        ("t7","云计算"),
        ("t8","其他"),
    )
    trade = models.CharField(verbose_name="行业",choices=trades,default="t1",max_length=10)

    locations = (
        ("l1","北京"),
        ("l2","上海"),
        ("l3","广州"),
        ("l4","深圳"),
        ("l5","全国"),
        ("l6","其他"),
    )
    location = models.CharField(verbose_name="地区",choices=locations,default="l1",max_length=10)
    pub_time = models.DateTimeField(verbose_name="发布时间",default=datetime.now)
    read_counts = models.IntegerField(verbose_name="阅读次数",default=0)
    class Meta:
        verbose_name = "面经"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.title

class Comment(models.Model):
    """
    评论
    """
    comment = models.CharField(verbose_name="评论",max_length=100)
    pub_time = models.DateTimeField(verbose_name="发布时间",default=datetime.now)
    interview = models.ForeignKey(Interview,verbose_name="文章外链")
    user = models.ForeignKey(User,verbose_name="用户外键")
    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name

class Faq(models.Model):
    """
    常见问答
    """
    question = models.CharField(verbose_name="问题",max_length=100,default="")
    answer = models.TextField(verbose_name="回答",max_length=500,default="")
    image = models.ImageField(verbose_name="问答图片",upload_to="faq/%Y/%m",blank=True,null=True)

    class Meta:
        verbose_name = "问答"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.question