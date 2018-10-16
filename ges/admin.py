from django.contrib import admin
from .models import Cloud, Datanode, Alarm
# Register your models here.


@admin.register(Cloud)
class CloudAdmin(admin.ModelAdmin):
    list_display = ('cloudid', 'cloudname', 'pub_date')
    list_display_links = ('cloudid', 'cloudname', 'pub_date')


@admin.register(Datanode)
class DataAdmin(admin.ModelAdmin):
    list_display = ('cloudid', 'dataunitid', 'dataunitip', 'pub_date')
    list_display_links = ('cloudid', 'dataunitid', 'dataunitip', 'pub_date')


@admin.register(Alarm)
class AlarmAdmin(admin.ModelAdmin):
    list_display = ('cloudid', 'alarmid', 'paramter', 'describe', 'pub_time', 'end_time')
    list_display_links = ('cloudid', 'alarmid')
