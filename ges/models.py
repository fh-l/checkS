from django.db import models

# Create your models here.
class Cloud(models.Model):
    cloudid = models.CharField(max_length=200, null=False)
    cloudname = models.CharField(max_length=200, null=False)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cloudid

class Datanode(models.Model):
    cloudid = models.CharField(max_length=200, null=False)
    dataunitid = models.CharField(max_length=200, null=False)
    dataunitip = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)

class Alarm(models.Model):
    cloudid = models.CharField(max_length=200, null=False)
    alarmid = models.CharField(max_length=200, null=False)
    paramter = models.CharField(max_length=1000, null=False)
    describe = models.CharField(max_length=1000, null=True)
    pub_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now=True)