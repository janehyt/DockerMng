# -*- coding: UTF-8 -*- 
from django.db import models
from django.contrib.auth.models import User

class Image(models.Model):
	CREATING = "CR"
	PULLING="PU"
	EXISTED="EX"
	ERROR="ER"
	STATUS_CHOICES=(
		(CREATING,"Creating"),
		(PULLING,"Pulling"),
		(EXISTED,"Existed"),
		(ERROR,"Error")
	)
	name = models.CharField(max_length = 150)
	status = models.CharField(max_length=2,
		choices=STATUS_CHOICES,
		default=CREATING)
	tag = models.CharField(max_length = 30)
	users = models.ManyToManyField(User)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	class Meta:
		unique_together=(('name','tag'),)

	def __unicode__(self):
		return self.name+":"+self.tag
	def to_start_pull(self):
		return self.status==Image.CREATING
	def is_pulling(self):
		return self.status==Image.PULLING
	def is_existed(self):
		return self.status==Image.EXISTED
# Create your models here.
class Container(models.Model):
	CREATING = "CR"
	EXISTED = "EX"
	ERROR = "ER"
	STATUS_CHOICES = (
		(CREATING, 'Creating'),
		(EXISTED, 'Existed'),
		(ERROR, 'Error')
	)

	name = models.CharField(max_length = 150,unique=True)
	status = models.CharField(max_length=2,
		choices=STATUS_CHOICES,
		default=CREATING)
	command = models.CharField(max_length = 150,default="")
	ports = models.CharField(max_length = 150,default="")
	volumes = models.CharField(max_length = 150,default="")
	links = models.CharField(max_length = 150,default="")
	envs = models.CharField(max_length = 150,default="")
	restart = models.BooleanField(default=False)
	image = models.ForeignKey(Image,on_delete=models.CASCADE)
	user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="owner")
	
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return self.name
	def to_pull(self):
		image = self.image
		if self.status==Container.CREATING:
			return image.to_start_pull()
		return False
	def is_pulling(self):
		image = self.image
		if self.status==Container.CREATING:
			return image.is_pulling()
		return False
	def is_existed(self):
		return self.status==Container.EXISTED
	def to_run(self):
		image = self.image
		if self.status==Container.CREATING:
			return image.is_existed()
		return False


class Progress(models.Model):
	id = models.CharField(primary_key=True,max_length = 12)
	status = models.CharField(max_length = 100)
	image = models.ForeignKey(Image,on_delete=models.CASCADE,
		related_name="progresses",related_query_name="progress")
	detail = models.CharField(blank=True,max_length = 150)
	pr = models.CharField(blank=True,max_length = 150)

	def __unicode__(self):
		return self.id