from django.db import models


class NodeManager(models.Manager):
    def create_node(self, manufacturer, nodeid):
        node = self.create(manufacturer=manufacturer, nodeid=nodeid)
        return node


class Node(models.Model):
    nodeid = models.CharField(max_length=200, null=False)
    manufacturer = models.CharField(max_length=200, null=False)
    pub_date = models.DateTimeField(auto_now_add=True)

    objects = NodeManager()

    def __str__(self):
        return self.manufacturer + '-' + self.nodeid


class Alarm(models.Model):
    cloudip = models.CharField(max_length=200, null=False)
    alarmid = models.CharField(max_length=200, null=False)
    paramter = models.CharField(max_length=1000, null=False)
    describe = models.CharField(max_length=1000, null=True)
    pub_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now=True)


class Datanode(models.Model):
    cloudip = models.CharField(max_length=200, null=False)
    dataunitip = models.CharField(max_length=200, null=False)
    pub_date = models.DateTimeField(auto_now_add=True)


class Cloud(models.Model):
    cloudip = models.CharField(max_length=200, null=False)
    cloudname = models.CharField(max_length=200, null=False)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cloudip
