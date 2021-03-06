#!/usr/bin/env python
# encoding: utf-8
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cloud/add', views.cloud_add, name='cloud_add'),
    path('cloud/alarm', views.alarm_add, name='alarm_add'),
    path('cloud/recover', views.alarm_recover, name='alarm_recover'),
    path('cloud/<str:cloudid>', views.cloud_delete, name='cloud_delete'),
    path('dataunit/add', views.datanode_add, name='datanode_add'),
    path('dataunit/<str:cloudid>/<str:dataunitid>', views.datanode_delete, name='datanode_delete')
]