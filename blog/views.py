# -*- coding: utf-8 -*-
from django.shortcuts import render,HttpResponse
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect,JsonResponse
from django.db.models import Q
import util
from util import check_post,check_login,re_js,create_html,find_data,Page
import json
from django.contrib.auth.models import User
from django.contrib import auth
from django import template 
import os
import time

# 数据库导入
from blog.models import Article
    
# Create your views here.

# 根地址跳转至home
def index(request):
    return HttpResponseRedirect(reverse("home"))


# 主页
def home(request):
    '''
    主页

    '''
    
    if  request.user.is_authenticated():
        # 登陆处理
        welcome = u"欢迎:%s" % (request.user.username)

        url_logout = reverse("logout")

        nav_right = u'<a href="%s">登出</a>' % url_logout

        url_new = reverse("add_article")

        nav_left = u'<a href="%s">新建</a>' % url_new
    else:

        url_login = reverse("login",args=(u"log_in",))
        url_logup = reverse("login",args=(u"log_up",))
        welcome = ""
        nav_right=u"<a href='%s'>登陆</a>" % url_login
        nav_left = u"<a href='%s'>注册</a>" % url_logup
        # r"<a href='../log_up'>注册</a>"

    # 文章列表
    obj = Article.objects.all()
    # 每页最多20条记录
    page = Page(obj)
    pagecount = page.page_count()

    obj = obj[0:10]

    if obj.count()==0:
        html = u'<h1>没有文章!</h1>'
    else:
        html = create_html(request,obj)

    return render(request,"home.html",{"welcome":welcome,"nav_right":nav_right,"nav_left":nav_left,"html":html,'pagecount':pagecount,"pagenum":1,})


# 登陆页面
def login(request,tag):
    '''
    登陆页面
    '''
    if tag == "log_in":
        return render(request,"log_in.html")
    if tag == "log_up":
        return render(request,"log_up.html")

# 验证码
def ajax_captcha(request):
    '''验证码获取'''
    cap=util.Captcha()
    cap.creat()
    request.session['cap']=cap.get_chars().lower()
    request.session['time']=time.time()
    img=cap.get_byte()
    return HttpResponse(img,"image/gif")


# 登陆数据处理
@check_post
def ajax_login(request):
    '''
    登陆验证
    '''
    # 获取数据
    try:
        username = request.POST.get("user")
        pwd = request.POST.get("pwd")
        cap = request.POST.get("cap")
    except Exception,msg:
        print(msg)
        msg="error|前端数据获取失败"
    else:

        try:
            caps = request.session.get("cap","")
            last_time = request.session.get("time",0)
        except:
            msg = "error|验证码获取失败!"
            print(msg)
        else:
            if not caps==cap or time.time()-last_time>30:
                msg="error|验证码错误或过期"
            else:
                try:
                    User.objects.get(username=username)
                except:
                    msg = "error|无此用户"
                    print(msg)
                else:
                    # 用户验证
                    user = auth.authenticate(username=username,password=pwd)

                    if user is not None and user.is_active:
                        # 用户登陆
                        auth.login(request,user)
                        msg = "ok|验证通过"
                    else:
                        msg = "error|密码错误"

    return JsonResponse({"msg":msg})


# 注册
@check_post
def ajax_logup(request):
    '''
    注册
    '''
    if request.method=="POST":
            # 获取数据
        try:
            username = request.POST.get("user")
            pwd = request.POST.get("pwd")
            cap = request.POST.get("cap")
        except Exception,msg:
            print(msg)
            msg = "error|前端数据获取失败"
        else:
            try:
                # 查询用户是否注册,注册则不会引发异常.
                User.objects.get(username=username)
            except:
                # 验证码获取
                s_cap = request.session.get("cap","")
                last_time = request.session.get("time",0)

                if not s_cap:
                    msg = "error|验证码异常"
                else:
                    if not cap.lower() == s_cap or time.time()-last_time>30:
                        msg = "error|验证码错误或过期"
                    else:
                        try:
                            # 用户创建
                            user = User.objects.create_user(username=username,password=pwd)
                            user.is_active=True
                            user.save()
                        except:
                            msg = "error|注册失败"
                        else:
                            msg = "ok|注册成功"
                            # 登陆
                            user = auth.authenticate(username=username,password=pwd)
                            auth.login(request,user)
            else:
                msg="error|用户已注册"

    return JsonResponse({"msg":msg})


# 登出
def logout(request):
    # 退出
    auth.logout(request)
    return HttpResponseRedirect(reverse("home"))


# 新建/编辑文章

@check_login
def add_article(request,id=""):
    name = request.user.username
    t = time.strftime("%Y-%m-%d")

    if id:
        id = int(id)
        try:
            obj = Article.objects.get(id=id)
        except Exception as e:
            print(e)
            return HttpResponse("<h1>文章获取失败!</h1>")
        else:
            
            return render(request,"article.html",{"name":name,"time":t,"obj":obj,"btn":"修改"})
    else:
        return render(request,"article.html",{"name":name,"time":t,"btn":"新建"})

# 文章保存
@check_post
@check_login
def ajax_editor(request):
    # 保存文章
    # 获取作者
    user = request.user
    if not user:
        msg = "error|无法获取作者"
    else:
    # 获取前段数据    
        try:
            html = request.POST.get("html","")
            title = request.POST.get("title","")
            tag = request.POST.get("tag","")
            keys = request.POST.get("keys","")
            id = request.POST.get("id","")
        except Exception as e:
            print(e)
            msg = u"error|前端数据获取失败"
            print msg
        else:
            # 前端没有id传过来则新建
            # 有id传过来则更新
            if not id:
            # script过滤
                html = re_js(html)
                title = re_js(title)
                tag = re_js(tag)
                keys = re_js(keys)

                try:
                    article = Article(title=title,
                                      user = user,
                                      article_class=tag,
                                      keyword=keys,
                                      content = html)
                    article.save()
                except Exception as e:
                    print(e)
                    msg = "error|文章保存失败"
                else:
                    msg = "ok|保存成功"
            else:
                try:
                    article = Article.objects.filter(id=id)
                    # 权限检查 操作和数据库中记录的用户不是一个人则抛出异常,无权修改.超级管理员有权修改
                    if article[0].user == user or user.is_superuser:
                        article.update(title=title,
                                       user = user,
                                       article_class=tag,
                                       keyword=keys,
                                       content = html)
                    else:
                        msg ="error|你没有修改权限"
                        print(msg)
                        raise Exception(msg)
                except Exception as e:
                    print(e)
                    msg = "error|更新失败"
                else:
                    msg = "ok|更新成功"
    return HttpResponse(msg)

# 文章显示页面
def show_article(request,id):
    id = int(id)

    try:
        obj = Article.objects.get(id=id)
        user = obj.user
    except Exception as e:
        msg = "error|文章获取失败"
        print(e+"|"+msg)
        return HttpResponse("<h1>文章获取失败</h1>")
    else:
        # 本用户则会有编辑按钮显示 
        if request.user==user:
            prompt = '<a href="/blog/editor_article/%s/">编辑</a>' % id
        else:
            prompt=""
        return render(request,"show_article.html",{"obj":obj,"prompt":prompt})

#删除文章
@check_post
@check_login
def ajax_del(request):
    # 获取数据
    try:
        id = request.POST.get("id","")
    except Exception as e:
        msg = "error|前端数据获取失败"
        print("%s|%s"%(msg,e))
    else:
        article = Article.objects.get(id=id)
        if not article.user == request.user or request.user.is_superuser:
            msg="error|删除失败"
        else:
            article.delete()
            msg="ok|删除成功"

    return HttpResponse(msg)


#总页码生成
@check_post
def ajax_pagecount(request):
    try:
        finddata = json.loads(request.POST.get("data"))
    except Exception as e:
        msg = "error|前端数据获取失败"
        print("%s'|'%s"%(msg,e))
    else:
       
        obj = find_data(finddata)
        page_obj = Page(obj)
        num = page_obj.page_count()
        # print(num)
        num =unicode(num)
        return HttpResponse(num)


# 主页文章标题列表显示    
@check_post
def ajax_titles(request):
    try:
        finddata = json.loads(request.POST.get("data"))
        page = int(request.POST.get("page"))
    except Exception as e:
        msg = "error|前端数据获取失败"
        print("%s'|'%s"%(msg,e))
    else:
        # print(finddata)
        obj = find_data(finddata)
        # print(obj)
        page_obj = Page(obj)
        obj = page_obj.page_obj(page)

        if obj.count()==0:
            html = u'<h2>没有文章!</h2>'
        else:
            html = create_html(request,obj)

        return HttpResponse(html)

















        
    


 









