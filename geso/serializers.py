#!/usr/bin/env python
# encoding: utf-8
from rest_framework import serializers


class CloudSerializer(serializers.Serializer):
    cloudip = serializers.CharField(required=True)
    totalspace = serializers.CharField(required=True)
    dataunitnum = serializers.CharField(required=True)
    subspacenum = serializers.CharField(required=True)
    raid = serializers.CharField(required=False)
    duplicate = serializers.CharField(required=True)
    manufacturer = serializers.CharField(required=True)
    admin = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    cloudname = serializers.CharField(required=True)
    metadatatype = serializers.CharField(required=True)
    metadataip = serializers.CharField(required=True)
    baseurl = serializers.CharField(required=True)
    area_code = serializers.CharField(required=True)
    protocol = serializers.CharField(required=True)



class DatanodeSerializer(serializers.Serializer):
    cloudip = serializers.CharField(required=True)
    dataunitip = serializers.CharField(required=True)
    totalspace = serializers.CharField(required=True)
    disknumber = serializers.CharField(required=True)
    dataunitname = serializers.CharField(required=True)
    dataunitcount = serializers.CharField(required=True)
    dataunittype = serializers.CharField(required=True)


class AlarmSerializer(serializers.Serializer):
    cloudip = serializers.CharField(required=True)
    time = serializers.CharField(required=True)
    type = serializers.CharField(required=True)
    paramter = serializers.JSONField(required=True)


class RecoverSerializer(serializers.Serializer):
    alarmid = serializers.CharField(required=True)
    time = serializers.CharField(required=True)
    describe = serializers.JSONField(required=True)

