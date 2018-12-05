import logging
import json
import uuid
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from .models import Node, Cloud, Datanode, Alarm
from .serializers import CloudSerializer, DatanodeSerializer, AlarmSerializer, RecoverSerializer

logger = logging.getLogger(__name__)


# Create your views here.
def getdataunitnum(request, manufacturer):
    logger.info(request.body)
    _uuid = uuid.uuid1()
    nodeid = str(_uuid).replace('-', '')
    manufacturer = manufacturer
    if request.method == 'POST':
        Node.objects.create_node(manufacturer=manufacturer, nodeid=nodeid)
        res = {"code": "200", "dataunitcount": nodeid}
        return JsonResponse(res, status=200)
    else:
        res = {"code": "-1", "message": "method not supported"}
        return JsonResponse(res, status=500)


@api_view(['POST'])
def cloud_add(request):
    datafrom = json.loads(request.GET.get('datafrom'))
    serializer = CloudSerializer(data=datafrom)
    if datafrom:
            Cloud.objects.create(cloudname=datafrom['cloudname'], cloudip=datafrom['cloudip'])
            return JsonResponse({'code': "200"}, status=200)

    else:
        return JsonResponse({"code": "-1", "message": serializer.errors}, status=500)


@api_view(['POST'])
def cloud_test(request):
    return JsonResponse({'code': "200", 'message': "connected success"}, status=200)



def cloud_delete(request, cloudip):
    logger.info(request.body)
    cloudip = cloudip
    if request.method == 'DELETE':
        try:
            cloud = Cloud.objects.get(cloudip=cloudip)
            cloud.delete()
            res = {"code": "200"}
            return JsonResponse(res, status=200)
        except Cloud.DoesNotExist:
            res = {"code": "-1", "message": "object not found"}
            return JsonResponse(res, status=200)
    else:
        res = {"code": "-1", "message": "method2 not supported"}
        return JsonResponse(res, status=200)


@api_view(['POST'])
def datanode_add(request):
    datafrom = json.loads(request.GET.get('datafrom'))
    serializer = DatanodeSerializer(data=datafrom)
    if serializer.is_valid():
        try:
            cloudip = serializer.validated_data['cloudip']
            logger.info(cloudip)
            print(cloudip)
            Cloud.objects.filter(cloudip=cloudip)
            dataunitip = serializer.validated_data['dataunitip']
            Datanode.objects.create(cloudip=cloudip, dataunitip=dataunitip)
            return JsonResponse({'code': "200"}, status=200)
        except Cloud.DoesNotExist:
            return JsonResponse({"code": "-1", "message": "cloudip not found"}, status=500)
    else:
        print('test1')
        return JsonResponse({"code": "-1", "message": serializer.errors}, status=500)


def datanode_delete(request, cloudip, dataunitip):
    cloudip = cloudip
    dataunitip =dataunitip

    if request.method == 'DELETE':
        try:
            dataunit = Datanode.objects.get(cloudip=cloudip, dataunitip=dataunitip)
            dataunit.delete()
            res = {"code": "200"}
            return JsonResponse(res, status=200)
        except Datanode.DoesNotExist:
            res = {"code": "-1", "message": "object not found"}
            return JsonResponse(res, status=500)
    else:
        res = {"code": "-1", "message": "method not supported"}
        return JsonResponse(res, status=500)


@api_view(['POST'])
def alarm_add(request):
    datafrom = json.loads(request.GET.get('datafrom'))
    serializer = AlarmSerializer(data=datafrom)
    if serializer.is_valid():
        try:
            cloudip = serializer.validated_data['cloudip']
            Cloud.objects.get(cloudip=cloudip)
            _uuid = uuid.uuid1()
            alarmid = str(_uuid).replace('-', '')
            Alarm.objects.create(alarmid=alarmid, cloudip=cloudip, paramter=json.dumps(datafrom))
            return JsonResponse({'code': "200", "alarmid": alarmid}, status=200)
        except Cloud.DoesNotExist:
            return JsonResponse({"code": "-1", "message": "cloudid not found"}, status=500)
    return JsonResponse({"code": "-1", "message": serializer.errors}, status=500)


@api_view(['POST'])
def alarm_recover(request):
    datafrom = json.loads(request.GET.get('datafrom'))
    serializer = RecoverSerializer(data=datafrom)
    if serializer.is_valid():
        alarmid = serializer.validated_data['alarmid']
        try:
            alarm = Alarm.objects.get(alarmid=alarmid)
            alarm.describe = json.dumps(datafrom)
            alarm.save()
            return JsonResponse({'code': "200"}, status=200)
        except Alarm.DoesNotExist:
            return JsonResponse({"code": "-1", "message": "alarmid not found"}, status=200)
    return JsonResponse({"code": "-1", "message": serializer.errors}, status=400)