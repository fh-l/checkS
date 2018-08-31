#!/usr/bin/env python
# encoding: utf-8
'''
@author: yao.qiang
@contact: yao.qiang@sihuatech.com
@file: urls.py
@time: 2018/8/31 17:13
@desc:
'''
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]