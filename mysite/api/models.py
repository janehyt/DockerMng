# -*- coding: UTF-8 -*-
'''models'''
import json
import os
import random
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
    private = models.BooleanField(default=True)


    def __unicode__(self):
        return self.name

class Repository(models.Model):
    '''Repository'''
    LOCAL = "local"
    name = models.CharField(max_length=150)
    namespace = models.CharField(max_length=150, default=LOCAL)
    user = models.ForeignKey(User, on_delete=models.CASCADE, \
            verbose_name="owner", related_name="repositories")
    description = models.TextField(default="", blank=True, null=True)
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
    builddir = models.CharField(default="", blank=True, null=True, max_length=150)

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
    status = models.CharField(max_length=100, blank=True,null=True,default="")
    image = models.ForeignKey(Image, on_delete=models.CASCADE,\
        related_name="processes", related_query_name="process")
    detail = models.TextField(blank=True, null=True, default="")
    proc = models.CharField(blank=True, null=True, default="",max_length=150)

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
    command = models.CharField(max_length=150, default="", blank=True, null=True)
    restart = models.BooleanField(default=False)
    image = models.ForeignKey(Image, on_delete=models.CASCADE,\
        related_name="containers")
    user = models.ForeignKey(User, on_delete=models.CASCADE,\
        verbose_name="owner", related_name="containers")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __unicode__(self):
        return self.name

    def create_ports(self,ports):
        ports = ports.split(",")
        for p in ports:
            if ":" in p:
                port = Port(port=p[0:len(p)-1],external=True)
                port.set_expose()
                self.ports.add(port,bulk=False)
            else:
                port = Port(port=p,external=False)
                self.ports.add(port,bulk=False)

    def create_environments(self,envs):
        envs = envs.split(",")
        for e in envs:
            data = e.split("=")
            if len(data) is 2:
                env = Environment(key=data[0],value=data[1])
                self.environments.add(env,bulk=False)
    def create_links(self,links):
        links = links.split(",")
        for l in links:
            data = l.split(":")
            if len(data) is 2:
                cons = Container.objects.filter(name=data[0])
                if len(cons) is 1:
                    link = Link(link=cons[0],alias=data[1])
                    self.links.add(link,bulk=False)

    def display_ports(self):

        result = {}
        for port in self.ports.all():
            result[port.port] = {"key":port.port,\
            "value":port.expose if port.external else port.external}
        return result

    def display_binds(self):
        result = {}
        for bind in self.binds.all():
            result[bind.path] = {"key": bind.path, \
                "value":bind.volume.name if bind.volume.private else bind.volume.path}
        return result

    def display_links(self):
        result = {}
        for link in self.links.all():
            result[link.link.name] = {"key":link.alias,"value":link.link.name,"id":link.link.id}
        return result
    def display_environments(self):
        result = {}
        for env in self.environments.all():
            result[env.key] = {"key":env.key,"value":env.value}
        return result
    def display_config(self):
        params = {"links":self.display_links(), "binds":self.display_binds(),\
            "ports":self.display_ports(), "envs":self.display_environments(),\
            "image":{},"command":[],\
            "restart":self.restart}
        image = self.image.repository.split("/")
        if len(image) is 2:
            params["image"]["namespace"] = image[0]
            params["image"]["name"] = image[1]
        else:
            params["image"]["namespace"] = "library"
            params["image"]["name"] = image[0]
        params["image"]["tag"] = self.image.tag
        if self.command:
            params["command"] = self.command.split(",")

        return params

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
    expose = models.CharField(default="", blank=True, null=True, max_length=5)

    class Meta:
        '''Meta'''
        unique_together = (('container', 'port'),)

    def __unicode__(self):
        return str(self.port)+ (":"+self.expose if self.external else "")

    def set_expose(self):
        self.expose = self.__generate_port()

    def __generate_port(self):
        pscmd = "netstat -ntl |grep -v Active| grep -v Proto|awk '{print $4}'|awk -F: '{print $NF}'"
        procs = os.popen(pscmd).read()
        procarr = procs.split("\n")
        tt= random.randint(10000,65534)
        count = Port.objects.filter(expose=tt).count()
        if tt not in procarr and count is 0:
            return tt
        else:
            self.generate_port()

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
