from django.db import models
import django.utils.timezone as timezone

# Create your models here.
class Cloud(models.Model):
    cloudid = models.CharField(max_length=200)
    pub_date = models.DateTimeField(default=timezone.now())

class Datanode(models.Model):
    cloudid = models.ForeignKey(Cloud, on_delete=models.CASCADE)
    dataunitid = models.CharField(max_length=200)

class Alarm(models.Model):
    cloudid = models.ForeignKey(Cloud, on_delete=models.CASCADE)
    alarmid = models.CharField(max_length=200)
    pub_time = models.DateTimeField(default=timezone.now())
    end_time = models.DateTimeField(auto_now=True)