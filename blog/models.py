# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Exuser(User):
    # 扩展user 添加等级字段
    graded = models.CharField(max_length=20)

class Article(models.Model):
    # 文章模型
    title=models.CharField(max_length=100)
    user = models.ForeignKey(User,related_name="articles")
    time = models.DateTimeField(auto_now=True)
    article_class = models.CharField(max_length=50,blank=True)
    keyword = models.CharField(max_length=100,blank=True)
    content = models.TextField(blank=True)

class Comment(models.Model):
    # 评论数据库
    articles = models.ForeignKey(Article,related_name="comments")
    name = models.CharField(max_length=50)
    text = models.TextField(blank=True)
    date = models.DateTimeField()


