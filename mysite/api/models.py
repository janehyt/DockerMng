# -*- coding: UTF-8 -*- 
from django.db import models
from django.contrib.auth.models import User
import json

class Volume(models.Model):
	name = models.CharField(max_length=150)
	path = models.CharField(max_length=250)
	user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="owner",related_name="volumes")
	readable = models.BooleanField(default=True)
	private = models.BooleanField(default=True)
	isfile = models.BooleanField(default=False)

	def __unicode__(self):
		return self.name

class Repository(models.Model):
	LOCAL="local"
	name = models.CharField(max_length=150)
	namespace = models.CharField(max_length=150,default=LOCAL)
	user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="owner",related_name="repositories")
	description=models.TextField(default="",blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		unique_together=(('name','namespace'),)

	def __unicode__(self):
		return self.namespace+"/"+self.name
	def get_absolute_url(self):
		return "/"+self.name+"/?namespace="+self.namespace

	def tagCount(self):
		return Image.objects.filter(repository=unicode(self)).count()

class Image(models.Model):
	PULLING = "PU"
	BUILDING = "BD"
	EXISTED = "EX"
	ERROR = "ER"
	STATUS_CHOICES=(
		(PULLING,"pulling"),
		(BUILDING,"building"),
		(EXISTED,"existed"),
		(ERROR,"error"),
	)
	repository=models.CharField(max_length=250)
	tag = models.CharField(max_length=150)
	users = models.ManyToManyField(User,related_name="images")
	status = models.CharField(max_length=2,
		choices=STATUS_CHOICES,default=PULLING)
	isbuild = models.BooleanField(default=False)
	builddir = models.CharField(default="",blank=True,max_length=150)
	class Meta:
		unique_together=(('repository','tag'),)
	def __unicode__(self):
		return self.repository+":"+self.tag

	def get_absolute_url(self):
		if self.id:
			return "/"+self.id
		else:
			return ""

#拉取进度或构建进度
class Process(models.Model):
	DEFAULT="000000000000"
	pid = models.CharField(max_length = 150,default=DEFAULT)
	status = models.CharField(max_length = 100,blank=True)
	image = models.ForeignKey(Image,on_delete=models.CASCADE,
		related_name="processes",related_query_name="process")
	detail = models.TextField(blank=True,default="")
	pr = models.CharField(blank=True,max_length = 150)
	class Meta:
		unique_together=(('pid','image'),)


	def __unicode__(self):
		return self.id
	def getDetail(self):
		result={}
		# if len(self.detail)>0:
		result=json.loads(self.detail)
		return result

class Container(models.Model):

	name = models.CharField(max_length = 150,unique=True)
	command = models.CharField(max_length = 150,default="",blank=True)
	
	restart = models.BooleanField(default=False)
	image = models.ForeignKey(Image,on_delete=models.CASCADE,related_name="containers")
	user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="owner",related_name="containers")
	
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.name
	def get_absolute_url(self):
		return "/"+self.id
# 容器连接情况
class Link(models.Model):
	container = models.ForeignKey(Container,on_delete=models.CASCADE,related_name="links")
	link = models.ForeignKey(Container,on_delete=models.CASCADE,related_name="services")
	alias = models.CharField(max_length=150)

	class Meta:
		unique_together=(('container','alias'),)

	def __unicode__(self):
		return unicode(self.link)+":"+alias
# 容器挂载情况
class Bind(models.Model):
	container = models.ForeignKey(Container,on_delete=models.CASCADE,related_name="binds")
	volume = models.ForeignKey(Volume,on_delete=models.CASCADE,related_name="binds")
	path = models.CharField(max_length= 250,default="/")

	class Meta:
		unique_together=(('container','path'),)

	def __unicode__(self):
			return unicode(self.volume)+":"+self.path
# 容器端口情况
class Port(models.Model):
	container=models.ForeignKey(Container,on_delete=models.CASCADE,related_name="ports")
	port = models.IntegerField()
	external = models.BooleanField(default=False)

	class Meta:
		unique_together=(('container','port'),)

	def __unicode__(self):
		return str(port)+(":" if external else "")

class Environment(models.Model):
	container=models.ForeignKey(Container,on_delete=models.CASCADE,related_name="environments")
	key = models.CharField(max_length=150,default="")
	value=models.CharField(max_length=150,default="")
	class Meta:
		unique_together=(('container','key'))

	def __unicode__(self):
		return key+"="+value

class Creation(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="dates")
	count = models.IntegerField(default=0)
	date = models.DateField(auto_now_add=True)
	class Meta:
		unique_together=(('user','date'),)