from django.db import models
import django.utils.timezone as timezone

# Create your models here.
class Cloud(models.Model):
    cloudid = models.CharField(max_length=200)
    pub_date = models.DateTimeField(default=timezone.now())

class Datanode(models.Model):
    cloudid = models.ForeignKey(Cloud, on_delete=models.CASCADE)
    dataunitid = models.CharField(max_length=200)