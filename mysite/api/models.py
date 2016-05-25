'''models'''
# -*- coding: UTF-8 -*-
import json
from django.db import models
from django.contrib.auth.models import User

class Volume(models.Model):
    '''
    # Volume
    '''
    name = models.CharField(max_length=150)
    path = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE, \
            verbose_name="owner", related_name="volumes")
    readable = models.BooleanField(default=True)
    private = models.BooleanField(default=True)
    isfile = models.BooleanField(default=False)


    def __unicode__(self):
        return self.name

class Repository(models.Model):
    '''Repository'''
    LOCAL = "local"
    name = models.CharField(max_length=150)
    namespace = models.CharField(max_length=150, default=LOCAL)
    user = models.ForeignKey(User, on_delete=models.CASCADE, \
            verbose_name="owner", related_name="repositories")
    description = models.TextField(default="", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        '''Meta'''
        unique_together = (('name', 'namespace'),)

    def __unicode__(self):
        return self.namespace+"/"+self.name


    def tag_num(self):
        '''
        # tag num
        '''
        return Image.objects.filter(repository=str(self)).count()

class Image(models.Model):
    '''Image'''
    PULLING = "PU"
    BUILDING = "BD"
    EXISTED = "EX"
    ERROR = "ER"
    STATUS_CHOICES = (\
        (PULLING, "pulling"),\
        (BUILDING, "building"),\
        (EXISTED, "existed"),\
        (ERROR, "error"),\
    )
    repository = models.CharField(max_length=250)
    tag = models.CharField(max_length=150)
    users = models.ManyToManyField(User, related_name="images")
    status = models.CharField(max_length=2,\
        choices=STATUS_CHOICES, default=PULLING)
    isbuild = models.BooleanField(default=False)
    builddir = models.CharField(default="", blank=True, max_length=150)

    class Meta:
        '''Meta'''
        unique_together = (('repository', 'tag'),)
    def __unicode__(self):
        return self.repository+":"+self.tag


#拉取进度或构建进度
class Process(models.Model):
    '''Process'''
    DEFAULT = "000000000000"
    pid = models.CharField(max_length=150, default=DEFAULT)
    status = models.CharField(max_length=100, blank=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE,\
        related_name="processes", related_query_name="process")
    detail = models.TextField(blank=True, default="")
    proc = models.CharField(blank=True, max_length=150)

    class Meta:
        '''Meta'''
        unique_together = (('pid', 'image'),)


    def __unicode__(self):
        return self.pid+":"+str(self.image)
    def get_detail(self):
        '''
        # detail json
        '''
        result = {}
        # if len(self.detail)>0:
        result = json.loads(self.detail)
        return result

class Container(models.Model):
    '''Container'''
    name = models.CharField(max_length=150, unique=True)
    command = models.CharField(max_length=150, default="", blank=True)
    restart = models.BooleanField(default=False)
    image = models.ForeignKey(Image, on_delete=models.CASCADE,\
        related_name="containers")
    user = models.ForeignKey(User, on_delete=models.CASCADE,\
        verbose_name="owner", related_name="containers")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __unicode__(self):
        return self.name

    def display_ports(self):
        result = ""
        for port in self.ports.all():
            result += unicode(port)
            result += ","
        if result:
            result = result[0:len(result)-1]
        return result
    def display_binds(self):
        result = ""
        for bind in self.binds.all():
            result += unicode(bind)
            result += ","
        if result:
            result = result[0:len(result)-1]
        return result
    def display_links(self):
        result = ""
        for link in self.links.all():
            result += unicode(link)
            result += ","
        if result:
            result = result[0:len(result)-1]
        return result

    def display_environments(self):
        result = ""
        for env in self.environments.all():
            result += unicode(env)
            result += ","
        if result:
            result = result[0:len(result)-1]
        return result
# 容器连接情况
class Link(models.Model):
    '''Link'''
    container = models.ForeignKey(Container, on_delete=models.CASCADE,\
        related_name="links")
    link = models.ForeignKey(Container, on_delete=models.CASCADE,\
        related_name="services")
    alias = models.CharField(max_length=150)


    class Meta:
        '''Meta'''
        unique_together = (('container', 'alias'),)

    def __unicode__(self):
        return str(self.link)+":"+self.alias
# 容器挂载情况
class Bind(models.Model):
    '''Bind'''
    container = models.ForeignKey(Container, on_delete=models.CASCADE,\
        related_name="binds")
    volume = models.ForeignKey(Volume, on_delete=models.CASCADE, \
        related_name="binds")
    path = models.CharField(max_length=250, default="/")


    class Meta:
        '''Meta'''
        unique_together = (('container', 'path'),)

    def __unicode__(self):
        return str(self.volume)+":"+self.path
# 容器端口情况
class Port(models.Model):
    '''Port'''
    container = models.ForeignKey(Container, on_delete=models.CASCADE,\
        related_name="ports")
    port = models.IntegerField()
    external = models.BooleanField(default=False)
    expose = models.CharField(default=None, blank=None, max_length=5)

    class Meta:
        '''Meta'''
        unique_together = (('container', 'port'),)

    def __unicode__(self):
        return str(self.port)+ (":" if self.external else "")

class Environment(models.Model):
    '''Environment'''
    container = models.ForeignKey(Container, on_delete=models.CASCADE,\
        related_name="environments")
    key = models.CharField(max_length=150, default="")
    value = models.CharField(max_length=150, default="")

    class Meta:
        '''Meta'''
        unique_together = (('container', 'key'))

    def __unicode__(self):
        return self.key+"="+self.value

class Creation(models.Model):
    '''Creation'''
    user = models.ForeignKey(User, on_delete=models.CASCADE,\
        related_name="dates")
    count = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)

    class Meta:
        '''Meta'''
        unique_together = (('user', 'date'),)
