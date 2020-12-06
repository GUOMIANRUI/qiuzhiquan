# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import User,Author,Interview,Faq

# Register your models here.

# 后台管理类 表名+admin

class UserAdmin(admin.ModelAdmin):
    list_display = ('username','email',)
    list_filter = ('username','email',) # 过滤器
    search_fields = ('username','email',) # 搜索框
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'desc',)
    list_filter = ('name', 'desc',)
    search_fields = ('name', 'desc',)

class InterviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'desc','company',)
    list_filter = ('title', 'desc','company',)
    search_fields = ('title', 'desc','company',)

class FaqAdmin(admin.ModelAdmin):
    list_display = ('question','answer',)
    list_filter = ('question','answer',)

admin.site.register(User,UserAdmin)
admin.site.register(Author,AuthorAdmin)
admin.site.register(Interview,InterviewAdmin)
admin.site.register(Faq,FaqAdmin)