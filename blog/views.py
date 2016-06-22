# -*- coding: utf-8 -*-
from django.shortcuts import render,HttpResponse
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect,JsonResponse
import util
from util import check_post,resolve

from django.contrib.auth.models import User
from django.contrib import auth
import os
import time

# Create your views here.

def home(request):
    '''
    主页

    '''
    
    # if "SERVER_SOFTWARE" in os.environ:
    #     data="true"
    # else:
    #     data="false"

    # env = os.environ

    
    if  request.user.is_authenticated():
        # 登陆处理
        welcome = u"欢迎:%s" % (request.user.username)
        url_logout = reverse("logout")

        nav_right = u'<a href="%s">登出</a>' % url_logout
        nav_left = u"新建"
    else:

        url_login = reverse("login",args=(u"log_in",))
        url_logup = reverse("login",args=(u"log_up",))
        welcome = ""
        nav_right=u"<a href='%s'>登陆</a>" % url_login
        nav_left = u"<a href='%s'>注册</a>" % url_logup
        # r"<a href='../log_up'>注册</a>"




    return render(request,"home.html",{"welcome":welcome,"nav_right":nav_right,"nav_left":nav_left})

def login(request,tag):
    '''
    登陆页面
    '''
    if tag == "log_in":
        return render(request,"log_in.html")
    if tag == "log_up":
        return render(request,"log_up.html")


def ajax_captcha(request):
    '''验证码获取'''
    cap=util.Captcha()
    cap.creat()
    request.session['cap']=cap.get_chars().lower()
    request.session['time']=time.time()
    img=cap.get_byte()
    return HttpResponse(img,"image/gif")

@check_post
def ajax_login(request):
    '''
    登陆验证
    '''
    # 获取数据
    try:
        username = resolve(request,"user",str)
        pwd  = resolve(request,"pwd",str)
        cap  = resolve(request,"cap",str)
    except Exception,msg:
        print(msg)
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

@check_post
def ajax_logup(request):
    '''
    注册
    '''
    if request.method=="POST":
            # 获取数据
        try:
            username = resolve(request,"user",str)
            pwd  = resolve(request,"pwd",str)
            cap  = resolve(request,"cap",str)
        except Exception,msg:
            print(msg)
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


def logout(request):
    # 退出
    auth.logout(request)
    return HttpResponseRedirect(reverse("home"))

