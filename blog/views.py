# -*- coding: utf-8 -*-
from django.shortcuts import render,HttpResponse
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
import util

# Create your views here.

def home(request):
    return render(request,"home.html")

def login(request,tag):
    if tag == "log_in":
        return render(request,"log_in.html")
    if tag == "log_up":
        return render(request,"log_up.html")


def ajax_captcha(request):
    # 验证码获取
    cap=util.Captcha()
    cap.creat()
    request.session['cap']=cap.get_chars().lower()
    img=cap.get_byte()
    return HttpResponse(img,"image/gif")
