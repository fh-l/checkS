from django.contrib import admin
from .models import Cloud, Datanode, Alarm, Node
# Register your models here.


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ('manufacturer', 'nodeid', 'pub_date')
    list_display_links = ('manufacturer', 'nodeid', 'pub_date')


@admin.register(Cloud)
class CloudAdmin(admin.ModelAdmin):
    list_display = ('cloudip', 'cloudname', 'pub_date')
    list_display_links = ('cloudip', 'cloudname', 'pub_date')


@admin.register(Datanode)
class DataAdmin(admin.ModelAdmin):
    list_display = ('cloudip', 'dataunitip', 'pub_date')
    list_display_links = ('cloudip', 'dataunitip', 'pub_date')


@admin.register(Alarm)
class AlarmAdmin(admin.ModelAdmin):
    list_display = ('cloudip', 'alarmid', 'paramter', 'describe', 'pub_time', 'end_time')
    list_display_links = ('cloudip', 'alarmid')
