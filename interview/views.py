# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect,render_to_response
from django.views.generic import View
from django.db.models import Q  # 导入一个或判断模块
from django.contrib.auth.hashers import make_password  # 导入密码加密模块
from forms import RegForm,LoginForm,CommentForm  # 导入用户表单（注册/登录/评论/）
from pure_pagination import Paginator,EmptyPage,PageNotAnInteger  # 导入分页库的类
from django.contrib.auth import logout,login,authenticate  # 导入用户登录/登出/认证
from django.core.urlresolvers import reverse  # 导入reverse解析模块（用来做重定向）
from django.http import HttpResponseRedirect,HttpResponse # 导入重定向模块

from models import Interview,Author,User,Comment,Faq  #  导入面经数据表/类
import ahocorasick
# Create your views here.

class InterListView(View):
    """
    名企面经列表类
    """

    def get(self,request):
        # 取出所有面经
        all_interviews = Interview.objects.all()  # 获取所有的面经对象（列表）

        # 点击搜索
        keywords = request.GET.get('keywords',"")
        if keywords:
            all_interviews = all_interviews.filter(Q(title__icontains=keywords)|Q(desc__icontains=keywords)|
                                                   Q(content__icontains=keywords))

        # 基于公司分类
        company = request.GET.get('company',"")
        if company:
            all_interviews = Interview.objects.filter(company = company)  # filter 查询公司名等于...的面经(可以查到 因为company这个键是Interview本身有的 没有的话得求助外键 比如year那个例子)

        # 基于行业分类
        trade = request.GET.get('trade', "")
        if trade:
            all_interviews = Interview.objects.filter(trade = trade)

        # 基于年级分类 (基于年级找作者 基于作者找面经)
        year = request.GET.get('year',"")
        if year:
            authors = Author.objects.filter(year = year)  # 取出这个年级对应的作者
            all_interviews = Interview.objects.none()

            for author in authors:
                interviews = author.interview_set.all()
                all_interviews = all_interviews | interviews


        # 对面经列表进行分页
        try:
            page = request.GET.get('page',1)
        except(PageNotAnInteger,EmptyPage):
            page = 1
        p = Paginator(all_interviews,2,request=request)  # 每一页显示2个
        interviews = p.page(page)

        return render(request,"interview_list.html",{
            "all_interviews": interviews,  # 传递模板变量给模板文件
        })

class InterDetailView(View):
    """
    面经详情
    """
    def get(self,request,interview_id):
        interview = Interview.objects.get(id=int(interview_id))  # 根据面经id（对应后台数据的id值 数据库数据表中有id）得到面经    这里过滤不能用filter 只能用get 针对唯一标识符

        # 增加阅读次数
        interview.read_counts +=1
        interview.save()

        # 推荐面经(同公司)
        company_tag = interview.company  # 命名为company_tag更好
        recommended_interviews = Interview.objects.filter(company=company_tag).exclude(id=int(interview_id)).order_by('-read_counts')[:3]

        # 更多面经（同行业）
        trade_tag = interview.trade  # 以行业作为标签  命名为trade_tag更好
        recommended_interviews2 = Interview.objects.filter(trade=trade_tag).exclude(company=company_tag).order_by('-read_counts')[:3]

        # 评论显示
        comments = Comment.objects.filter(interview=interview).order_by("-pub_time")

        return render(request,"interview_detail.html",{
            "interview": interview,
            "recommended_interviews": recommended_interviews,
            "recommended_interviews2": recommended_interviews2,
            "comments":comments,
        })  # 返回面经详情页

class RegView(View):
    """
    用户注册类
    """
    def get(self,request):
        return render(request,"reg.html",{})

    def post(self,request):
        regform = RegForm(request.POST)
        if regform.is_valid():
            username = request.POST.get("email","")
            email = request.POST.get("email","")
            password = request.POST.get("password","")
            user = User()
            user.username = username
            user.email = email
            user.password = password
            user.password = make_password(password)
            user.save()
            return render(request,"login.html", {})
        else:
            return render(request,"reg.html",{
                "regform":regform
            })

class LoginView(View):
    """
    用户登录类
    """
    def get(self,request):  # 用户访问登录
        return render(request,"login.html",{})
    def post(self,request):
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            username = request.POST.get("email","")
            password = request.POST.get("password","")
            user = authenticate(username = username,password = password)
            if user is not None:
                login(request,user)
            else:
                return render(request,"login.html",{"error":'登录验证失败'})
            return HttpResponseRedirect(reverse("index"))  # 重定向到首页
        else:
            return render(request,"login.html",{"error":'登录验证失败'})

class LogoutView(View):
    """
    用户注销（退出）
    """
    def get(self,request):
        logout(request)  # 退出
        return HttpResponseRedirect(reverse("index"))  # 重定向到首页

class IndexView(View):
    """
    首页
    """
    def get(self,request):
        all_interviews = Interview.objects.all().order_by("-read_counts")[:6]
        return render(request, "index.html", {
            "all_interviews": all_interviews,
        })

class AddCommentView(View):
    """
    添加评论
    """
    def post(self,request,interview_id):
        interview = Interview.objects.get(id=int(interview_id))
        if request.user.is_authenticated():  #如果登录成功 进入表单验证
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():  # 如果表单有效，则保存评论信息
                content = request.POST.get('comment')
                content_pr = str(content)
                wordlist = ['卧槽','狗东西','傻逼','你他妈','滚','老子','你大爷的','    草泥马','转帐']
                actree = ahocorasick.Automaton()
                for index, word in enumerate(wordlist):
                    actree.add_word(word, (index, word))
                actree.make_automaton()
                content = content_pr
                for i in actree.iter(content_pr):
                    content = content.replace(i[1][1], "**")
                comments = Comment()
                comments.comment = content
                comments.user = request.user
                comments.interview = interview
                comments.save()
                return redirect(request.META['HTTP_REFERER'])  # 若表单内容已经保存，则刷新本页面
            else:
                return HttpResponse("请输入正确的评论")  # 若表单信息无效,给用户错误警告
        else:  # 如果登录失败或用户未登录，则重定向/返回到登录页面
            return render(request,"login.html", {
                "error":"请登录后再评论"
            })

class ContactView(View):
    """
    联系页
    """
    def get(self,request):
        return render(request,"contact.html",{})
    
class FaqView(View):
    """
    常见问答
    """
    def get(self,request):
        all_faqs = Faq.objects.all()[:10]  # 获取所有问答
        return render(request,"faq.html",{
            "all_faqs": all_faqs,
        })

# http状态码：正常200 无网页404
def view_404(request):
    response = render_to_response('404.html',{})
    response.status_code = 404
    return response

def view_500(request):
    response = render_to_response('500.html',{})
    response.status_code = 500
    return response