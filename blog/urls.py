# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    # 主页
    url(r'^home/$',views.home,name="home"),
]

log_patterns=[
   # 登陆 

   # 登陆注册
    url(r'^(?P<tag>(log_in|log_up))/$',views.login,name="login"),


   # 验证码
    url(r'^ajax_captcha/$',views.ajax_captcha,name="capticha"),

    # 登陆
    url(r'^ajax_login/$',views.ajax_login,name="ajax_login"),
    # 注册
    url(r'^ajax_logup$',views.ajax_logup,name="ajax_logup"),
]


urlpatterns.extend(log_patterns)
