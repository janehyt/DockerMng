# -*- coding: UTF-8 -*- 
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Container(models.Model):
	name = models.CharField(max_length = 150,unique=True)
	state = models.BooleanField(default=True)#用于软删除
	command = models.CharField(max_length=150)#启动命令
	user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="owner")
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return self.name

class Image(models.Model):
	name = models.CharField(max_length = 150)
	state = models.BooleanField(default=True)#用于软删除
	tag = models.CharField(max_length = 30)
	user = models.ManyToManyField(User)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	class Meta:
		unique_together=(('name','tag'),)

	def __unicode__(self):
		return self.name