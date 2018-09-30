#!/usr/bin/env python
# encoding: utf-8
'''
@author: yao.qiang
@contact: yao.qiang@sihuatech.com
@file: serializers.py.py
@time: 2018/9/5 9:53
@desc:
'''
from rest_framework import serializers
from .models import Cloud, Datanode, Alarm


class CloudSerializer(serializers.Serializer):
    cloudname = serializers.CharField(required=True)
    cloudip = serializers.CharField(required=True)
    cloudname = serializers.CharField(required=True)
    totalspace = serializers.CharField(required=True)
    availablespace = serializers.CharField(required=True)
    dataunitnum = serializers.CharField(required=True)
    subspacenum = serializers.CharField(required=True)
    raid = serializers.CharField(required=False)
    duplicate = serializers.CharField(required=True)
    manufacturer = serializers.CharField(required=True)
    productmodel = serializers.CharField(required=True)
    metadatatype = serializers.CharField(required=True)
    #metadataip = serializers.CharField(required=True)
    areacode = serializers.CharField(required=True)
    protocol = serializers.CharField(required=True)



class DatanodeSerializer(serializers.Serializer):
    cloudid = serializers.CharField(required=True)
    dataunitip = serializers.CharField(required=True)
    totalspace = serializers.CharField(required=True)
    disknumber = serializers.CharField(required=True)
    dataunitname = serializers.CharField(required=True)
    dataunittype = serializers.CharField(required=True)
    availablespace = serializers.CharField(required=True)


class AlarmSerializer(serializers.Serializer):
    cloudid = serializers.CharField(required=True)
    time = serializers.CharField(required=True)
    type = serializers.CharField(required=True)
    paramter = serializers.JSONField(required=True)


class RecoverSerializer(serializers.Serializer):
    alarmid = serializers.CharField(required=True)
    time = serializers.CharField(required=True)
    describe = serializers.JSONField(required=True)

