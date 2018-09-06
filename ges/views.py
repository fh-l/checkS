import json
import uuid
import logging
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from .models import Cloud, Datanode, Alarm
from .serializers import CloudSerializer, DatanodeSerializer, AlarmSerializer, RecoverSerializer

logger = logging.getLogger(__name__)


def check_headers(headers):
    common = ['HTTP_VERSION', 'HTTP_DATE', 'HTTP_SIGNATURE', 'HTTP_STORAGEKEYID']
    for key in common:
        if key not in headers:
            return False
    else:
        return True


def index(request):
    return HttpResponse('Hello World!')


@api_view(['POST'])
def cloud_add(request):
    logger.info(request.META)
    serializer = CloudSerializer(data=request.data)
    if serializer.is_valid():
        cloudid = uuid.uuid1()
        Cloud.objects.create(cloudname=serializer.validated_data['cloudname'], cloudid=cloudid)
        return JsonResponse({'code': "200", "cloudid": cloudid}, status=200)
    return JsonResponse({"code": "1", "message": serializer.errors}, status=400)


def cloud_delete(request, cloudid):
    if check_headers(headers=request.META):
        if request.method == 'DELETE':
            try:
                cloud = Cloud.objects.get(cloudid=cloudid)
                cloud.delete()
                res = {"code": "200"}
                return JsonResponse(res, status=200)
            except Cloud.DoesNotExist:
                res = {"code": "500", "message": "object not found"}
                return JsonResponse(res, status=400)
        else:
            res = {"code": "500", "message": "method not supported"}
            return JsonResponse(res, status=400)
    else:
        res = {"code": "500", "message": "public header not contained"}
        return JsonResponse(res, status=400)


@api_view(['POST'])
def datanode_add(request):
    serializer = DatanodeSerializer(data=request.data)
    if serializer.is_valid():
        cloudid = serializer.validated_data['cloudid']
        try:
            Cloud.objects.get(cloudid=cloudid)
            dataunitid = uuid.uuid1()
            dataunitip = serializer.validated_data['dataunitip']
            Datanode.objects.create(cloudid=cloudid, dataunitid=dataunitid, dataunitip=dataunitip)
            return JsonResponse({'code': "200", "dataunitid": dataunitid}, status=200)
        except Cloud.DoesNotExist:
            return JsonResponse({"code": "1", "message": "cloudid not found"}, status=400)
    return JsonResponse({"code": "1", "message": serializer.errors}, status=400)


def datanode_delete(request, cloudid, dataunitid):
    if check_headers(headers=request.META):
        if request.method == 'DELETE':
            try:
                dataunit = Datanode.objects.get(cloudid=cloudid, dataunitid=dataunitid)
                dataunit.delete()
                res = {"code": "200"}
                return JsonResponse(res, status=200)
            except Datanode.DoesNotExist:
                res = {"code": "500", "message": "object not found"}
                return JsonResponse(res, status=400)
        else:
            res = {"code": "500", "message": "method not supported"}
            return JsonResponse(res, status=400)
    else:
        res = {"code": "500", "message": "public header not contained"}
        return JsonResponse(res, status=400)


@api_view(['POST'])
def alarm_add(request):
    serializer = AlarmSerializer(data=request.data)
    if serializer.is_valid():
        cloudid = serializer.validated_data['cloudid']
        paramter = serializer.validated_data['paramter']
        try:
            Cloud.objects.get(cloudid=cloudid)
            alarmid = uuid.uuid1()
            Alarm.objects.create(alarmid=alarmid, cloudid=cloudid, paramter=json.dumps(paramter))
            return JsonResponse({'code': "200", "alarmid": alarmid}, status=200)
        except Cloud.DoesNotExist:
            return JsonResponse({"code": "1", "message": "cloudid not found"}, status=400)
    return JsonResponse({"code": "1", "message": serializer.errors}, status=400)


@api_view(['POST'])
def alarm_recover(request):
    serializer = RecoverSerializer(data=request.data)
    if serializer.is_valid():
        alarmid = serializer.validated_data['alarmid']
        describe = serializer.validated_data['describe']
        try:
            alarm = Alarm.objects.get(alarmid=alarmid)
            alarm.describe = json.dumps(describe)
            alarm.save()
            return JsonResponse({'code': "200"}, status=200)
        except Alarm.DoesNotExist:
            return JsonResponse({"code": "1", "message": "alarmid not found"}, status=400)
    return JsonResponse({"code": "1", "message": serializer.errors}, status=400)
