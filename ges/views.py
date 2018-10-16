import json
import uuid
import logging
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from .utils import hash_hmac
from .models import Cloud, Datanode, Alarm
from .serializers import CloudSerializer, DatanodeSerializer, AlarmSerializer, RecoverSerializer

logger = logging.getLogger(__name__)
key = '123456'


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
    logger.info(request.body)
    logger.info(request.META)
    headers = request.META
    if check_headers(headers):
        serializer = CloudSerializer(data=request.data)
        if serializer.is_valid():
            logger.info(serializer.validated_data)
            userkeyid = headers['HTTP_STORAGEKEYID']
            time = headers['HTTP_DATE']
            version = headers['HTTP_VERSION']
            signature = headers['HTTP_SIGNATURE']
            cloudip = serializer.validated_data['cloudip']
            cloudname = serializer.validated_data['cloudname']
            totalspace = serializer.validated_data['totalspace']
            availablespace = serializer.validated_data['availablespace']
            dataunitnum = serializer.validated_data['dataunitnum']
            subspacenum = serializer.validated_data['subspacenum']
            raid = serializer.validated_data['raid']
            duplicate = serializer.validated_data['duplicate']
            manufacturer = serializer.validated_data['manufacturer']
            productmodel = serializer.validated_data['productmodel']
            metadatatype = serializer.validated_data['metadatatype']
            # metadataip = serializer.validated_data['metadataip']
            areacode = serializer.validated_data['areacode']
            protocol = serializer.validated_data['protocol']
            stringtosing = 'POST&UserKeyID={0}&Time={1}&Version={2}&cloudip={4}&cloudname={5}&totalspace={6}&' \
                           'availablespace={7}&dataunitnum={8}&subspacenum={9}&raid={3}&duplicate={10}&manufacturer={11}&productmodel={12}&' \
                           'metadatatype={13}&areacode={14}&protocol={15}'.format(
                userkeyid, time, version, raid, cloudip, cloudname, totalspace, availablespace, dataunitnum, subspacenum, duplicate, manufacturer,
                productmodel, metadatatype, areacode, protocol)
            sing = hash_hmac(stringtosing, key)
            logger.info("The origin string is: {0}".format(stringtosing))
            logger.info("The calculator signature is: {0}".format(sing))
            if sing == signature:
                if serializer.is_valid():
                    _uuid = uuid.uuid1()
                    cloudid = str(_uuid).replace('-', '')
                    Cloud.objects.create(cloudname=serializer.validated_data['cloudname'], cloudid=cloudid)
                    return JsonResponse({'code': "200", "cloudid": cloudid}, status=200)

            else:
                res = {"code": "-1", "message": "signature not equal"}
                return JsonResponse(res, status=200)
        else:
            return JsonResponse({"code": "-1", "message": serializer.errors}, status=200)

    else:
        res = {"code": "-1", "message": "public header not contained"}
        return JsonResponse(res, status=200)


def cloud_delete(request, cloudid):
    logger.info(request.body)
    logger.info(request.META)
    headers = request.META
    if check_headers(headers):
        cloudid = cloudid
        userkeyid = headers['HTTP_STORAGEKEYID']
        time = headers['HTTP_DATE']
        version = headers['HTTP_VERSION']
        signature = headers['HTTP_SIGNATURE']
        stringtosing = 'DELETE&UserKeyID={0}&Time={1}&Version={2}&cloudid={3}'.format(userkeyid, time, version, cloudid)
        sing = hash_hmac(stringtosing, key)
        logger.info("The origin string is: {0}".format(stringtosing))
        logger.info("The calculator signature is: {0}".format(sing))
        if sing == signature:
            if request.method == 'DELETE':
                try:
                    cloud = Cloud.objects.get(cloudid=cloudid)
                    cloud.delete()
                    res = {"code": "200"}
                    return JsonResponse(res, status=200)
                except Cloud.DoesNotExist:
                    res = {"code": "-1", "message": "object not found"}
                    return JsonResponse(res, status=200)
            else:
                res = {"code": "-1", "message": "method not supported"}
                return JsonResponse(res, status=200)
        else:
            res = {"code": "-1", "message": "signature not equal"}
            return JsonResponse(res, status=200)
    else:
        res = {"code": "-1", "message": "public header not contained"}
        return JsonResponse(res, status=400)


@api_view(['POST'])
def datanode_add(request):
    logger.info(request.body)
    logger.info(request.META)
    headers = request.META
    if check_headers(headers):
        serializer = DatanodeSerializer(data=request.data)
        if serializer.is_valid():
            logger.info(serializer.validated_data)
            userkeyid = headers['HTTP_STORAGEKEYID']
            time = headers['HTTP_DATE']
            version = headers['HTTP_VERSION']
            signature = headers['HTTP_SIGNATURE']
            cloudid = serializer.validated_data['cloudid']
            dataunitip = serializer.validated_data['dataunitip']
            totalspace = serializer.validated_data['totalspace']
            disknumber = serializer.validated_data['disknumber']
            dataunitname = serializer.validated_data['dataunitname']
            dataunittype = serializer.validated_data['dataunittype']
            availablespace = serializer.validated_data['availablespace']
            stringtosing = 'POST&UserKeyID={0}&Time={1}&Version={2}&cloudid={3}&' \
                           'dataunitip={4}&totalspace={5}&disknumber={6}&dataunitname={7}&' \
                           'dataunittype={8}&availablespace={9}'.format(
                userkeyid, time, version, cloudid, dataunitip, totalspace, disknumber,
                dataunitname, dataunittype, availablespace)
            sing = hash_hmac(stringtosing, key)
            logger.info("The origin string is: {0}".format(stringtosing))
            logger.info("The calculator signature is: {0}".format(sing))
            if sing == signature:
                try:
                    Cloud.objects.get(cloudid=cloudid)
                    _uuid = uuid.uuid1()
                    dataunitid = str(_uuid).replace('-', '')
                    dataunitip = serializer.validated_data['dataunitip']
                    Datanode.objects.create(cloudid=cloudid, dataunitid=dataunitid, dataunitip=dataunitip)
                    return JsonResponse({'code': "200", "dataunitid": dataunitid}, status=200)
                except Cloud.DoesNotExist:
                    return JsonResponse({"code": "-1", "message": "cloudid not found"}, status=400)
            else:
                res = {"code": "-1", "message": "signature not equal"}
                return JsonResponse(res, status=200)
        return JsonResponse({"code": "-1", "message": serializer.errors}, status=400)
    else:
        res = {"code": "-1", "message": "public header not contained"}
        return JsonResponse(res, status=400)


def datanode_delete(request, cloudid, dataunitid):
    headers = request.META
    if check_headers(headers):
        cloudid = cloudid
        dataunitid =dataunitid
        userkeyid = headers['HTTP_STORAGEKEYID']
        time = headers['HTTP_DATE']
        version = headers['HTTP_VERSION']
        signature = headers['HTTP_SIGNATURE']
        stringtosing = 'DELETE&UserKeyID={0}&Time={1}&Version={2}&cloudid={3}&dataunitid={4}'.format(
            userkeyid, time, version, cloudid, dataunitid)
        sing = hash_hmac(stringtosing, key)
        logger.info("The origin string is: {0}".format(stringtosing))
        logger.info("The calculator signature is: {0}".format(sing))
        if sing == signature:
            if request.method == 'DELETE':
                try:
                    dataunit = Datanode.objects.get(cloudid=cloudid, dataunitid=dataunitid)
                    dataunit.delete()
                    res = {"code": "200"}
                    return JsonResponse(res, status=200)
                except Datanode.DoesNotExist:
                    res = {"code": "-1", "message": "object not found"}
                    return JsonResponse(res, status=400)
            else:
                res = {"code": "-1", "message": "method not supported"}
                return JsonResponse(res, status=400)
        else:
            res = {"code": "-1", "message": "signature not equal"}
            return JsonResponse(res, status=200)
    else:
        res = {"code": "-1", "message": "public header not contained"}
        return JsonResponse(res, status=400)


@api_view(['POST'])
def alarm_add(request):
    logger.info(request.body)
    logger.info(request.META)
    headers = request.META
    if check_headers(headers):
        serializer = AlarmSerializer(data=request.data)
        if serializer.is_valid():
            logger.info(serializer.validated_data)
            userkeyid = headers['HTTP_STORAGEKEYID']
            time = headers['HTTP_DATE']
            version = headers['HTTP_VERSION']
            signature = headers['HTTP_SIGNATURE']
            cloudid = serializer.validated_data['cloudid']
            a_time = serializer.validated_data['time']
            type = serializer.validated_data['type']
            paramter = serializer.validated_data['paramter']
            if type == '1':
                paramtername = paramter['paramtername']
                value = paramter['value']
                dataunitid = paramter['dataunitid']
                stringtosing = 'POST&UserKeyID={0}&Time={1}&Version={2}&cloudid={3}&time={4}&type={5}&' \
                               'paramtername={6}&value={7}&dataunitid={8}'.format(
                    userkeyid, time, version, cloudid, a_time, type, paramtername, value, dataunitid)
            elif type == '2':
                disktype = paramter['disktype']
                position = paramter['position']
                dataunitid = paramter['dataunitid']
                alarmtype = paramter['alarmtype']
                message = paramter['message']
                stringtosing = 'POST&UserKeyID={0}&Time={1}&Version={2}&cloudid={3}&time={4}&type={5}&' \
                               'disktype={6}&position={7}&dataunitid={8}&alarmtype={9}&message={10}'.format(
                    userkeyid, time, version, cloudid, a_time, type, disktype, position, dataunitid, alarmtype, message)
            elif type == '3':
                dataunitid = paramter['dataunitid']
                dataunittype = paramter['dataunittype']
                alarmtype = paramter['alarmtype']
                detail = paramter['detail']
                stringtosing = 'POST&UserKeyID={0}&Time={1}&Version={2}&cloudid={3}&time={4}&type={5}&' \
                               'dataunitid={6}&power={9}&fan={10}&cpu={11}&dataunittype={7}&alarmtype={8}'.format(
                    userkeyid, time, version, cloudid, a_time, type, dataunitid, dataunittype, alarmtype, detail['power'], detail['fan'], detail['cpu'])

            elif type == '4':
                subspaceid = paramter['subspaceid']
                subspacesize = paramter['subspacesize']
                usedspace = paramter['usedspace']
                stringtosing = 'POST&UserKeyID={0}&Time={1}&Version={2}&cloudid={3}&time={4}&type={5}&' \
                               'subspaceid={6}&subspacesize={7}&usedspace={8}'.format(
                    userkeyid, time, version, cloudid, a_time, type, subspaceid, subspacesize, usedspace)
            else:
                stringtosing = ''
            sing = hash_hmac(stringtosing, key)
            logger.info("The origin string is: {0}".format(stringtosing))
            logger.info("The calculator signature is: {0}".format(sing))
            if sing == signature:
                try:
                    Cloud.objects.get(cloudid=cloudid)
                    _uuid = uuid.uuid1()
                    alarmid = str(_uuid).replace('-', '')
                    Alarm.objects.create(alarmid=alarmid, cloudid=cloudid, paramter=json.dumps(paramter))
                    return JsonResponse({'code': "200", "alarmid": alarmid}, status=200)
                except Cloud.DoesNotExist:
                    return JsonResponse({"code": "-1", "message": "cloudid not found"}, status=200)
            else:
                res = {"code": "-1", "message": "signature not equal"}
                return JsonResponse(res, status=200)
        return JsonResponse({"code": "-1", "message": serializer.errors}, status=200)
    else:
        res = {"code": "-1", "message": "public header not contained"}
        return JsonResponse(res, status=200)


@api_view(['POST'])
def alarm_recover(request):
    headers = request.META
    if check_headers(headers):
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
                return JsonResponse({"code": "-1", "message": "alarmid not found"}, status=400)
        return JsonResponse({"code": "-1", "message": serializer.errors}, status=400)
    else:
        res = {"code": "-1", "message": "public header not contained"}
        return JsonResponse(res, status=400)
