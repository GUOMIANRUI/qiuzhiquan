# -*- coding: utf-8 -*-
"""qiuzhiquan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.views.static import serve  # 模板文件图片解析模块
from settings import MEDIA_ROOT  #根据文件图片解析路径

from interview.views import InterListView,InterDetailView,RegView,LoginView,LogoutView,IndexView  # 导入Views函数/类
from interview.views import AddCommentView,ContactView,FaqView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^media/(?P<path>.*)$',serve,{"document_root":MEDIA_ROOT}),  # 管理媒体文件路径和处理模块
    url(r'^interlist/$', InterListView.as_view(),name="interlist"),  # 实现名企面经页面的映射
    url(r'^interdetail/(?P<interview_id>\d+)/$',InterDetailView.as_view(),name = "interdetail"),  # 面经映射详情
    url(r'^ueditor/',include('DjangoUeditor.urls')),  # 增加ueditor映射
    url(r'^register/$', RegView.as_view(), name = "register" ),  # 用户注册页映射
    url(r'^login/$', LoginView.as_view(), name = "login" ),  # 用户登页映射
    url(r'^logout/$', LogoutView.as_view(), name = "logout" ),  # 用户注销映射
    url(r'^$', IndexView.as_view(), name = "index" ),  # 首页映射
    url(r'^addcomment/(?P<interview_id>\d+)/$',AddCommentView.as_view(),name="addcomment"),  # 用户评论映射
    url(r'^contact/$',ContactView.as_view(),name="contact"),  # 联系页
    url(r'^faq/$',FaqView.as_view(),name="faq"),  # 问答页
]

# 404和500配置
handler404 = 'interview.views.view_404'  # 直接以绝对路径写 不用导
handler505 = 'interview.views.view_500'