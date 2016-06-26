# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    # 主页
    url(r'^home/$',views.home,name="home"),
    url(r"^about/$",views.about,name="about")
]
  


home_patterns=[
   # 主页

   # 登陆注册
    url(r'^(?P<tag>(log_in|log_up))/$',views.login,name="login"),
    #退出
    url(r'^logout/$',views.logout,name="logout"),


   # 验证码
    url(r'^ajax_captcha/$',views.ajax_captcha,name="capticha"),
    # 登陆
    url(r'^ajax_login/$',views.ajax_login,name="ajax_login"),
    # 注册
    url(r'^ajax_logup$',views.ajax_logup,name="ajax_logup"),

    # 标题列表获取
    url(r'^ajax_titles/$',views.ajax_titles,name="ajax_titles"),
    #获取总页码
    url(r'^ajax_pagecount/$',views.ajax_pagecount,name="ajax_pagecount")
    
    

]
urlpatterns.extend(home_patterns)


article_patterns=[
   # 文章编辑
   # 显示文章
    url(r'^show_article/(?P<id>[0-9]+)/$',views.show_article,name = "show_article"),

    # 添加文章 编辑页面
    url(r'^editor_article/(?P<id>[0-9]+)/$',views.add_article,name = "editor_article"),
    url(r'^add_article/$',views.add_article,name = "add_article"),
    #编辑文章
    url(r'^ajax_editor/$',views.ajax_editor,name="ajax_editor"),

    #删除文章
    url(r'^ajax_del/$',views.ajax_del,name="ajax_del"),


]
urlpatterns.extend(article_patterns)




