# -*- coding: UTF-8 -*- 
from django.db import models,connection
from django.contrib.auth.models import User
from . import files

import os,random,json

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
	users = models.ManyToManyField(User,related_name="image")
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	class Meta:
		unique_together=(('name','tag'),)

	def __unicode__(self):
		return self.name+":"+self.tag
	# def to_start_pull(self):
	# 	return self.status==Image.CREATING
	# def is_pulling(self):
	# 	return self.status==Image.PULLING
	# def is_existed(self):
	# 	return self.status==Image.EXISTED
	def get_absolute_url(self):
		return "/"+self.id
	def getDetailStatus(self):
		result={}
		if self.status==Image.CREATING:
			result["code"]=1
			result["detail"]="no image"
		elif self.status==Image.PULLING:
			result["code"]=2
			result["detail"]="pulling image"
		elif self.status==Image.EXISTED:
			result["code"]=3
			result["detail"]="done image"
		else:
			result["code"]=-1
			result["detail"]="error image"
		return result

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
	SELECT_DAY={'day':connection.ops.date_trunc_sql('day','created')}

	name = models.CharField(max_length = 150,unique=True)
	status = models.CharField(max_length=2,
		choices=STATUS_CHOICES,
		default=CREATING)
	command = models.CharField(max_length = 150,default="",blank=True)
	ports = models.CharField(max_length = 150,default="",blank=True)
	volumes = models.TextField(default="",blank=True)
	links = models.CharField(max_length = 150,default="",blank=True)
	envs = models.TextField(default="",blank=True)
	restart = models.BooleanField(default=False)
	image = models.ForeignKey(Image,on_delete=models.CASCADE,related_name="container")
	user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="owner",related_name="container")
	
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return self.name
	def __getitem__(self):
		return self.name
	def get_absolute_url(self):
		return "/"+self.id
	
	def getFullConfig(self):
		params={
			"image":{
				"name":self.image.name,
				"tag":self.image.tag,
				"namespace":"library"
			},
			"command":[],
			"ports":{},
			"volumes":{},
			"links":{},
			"envs":{},
			"restart":self.restart,
		}
		if "/" in self.image.name:
			name = self.image.name.split("/")
			params["image"]["namespace"]=name[0]
			params["image"]["name"]=name[1]
		if len(self.command)>0:
			params['command'] = self.command.split(",")
		if len(self.ports)>0:
			tmp={}
			ports=self.ports.split(",")
			for port in ports:
				if ":" in port:
					p =port.split(":")
					tmp[p[0]]={"key":p[0],"value":True}
				else:
					tmp[port]={"key":port,"value":False}
			params['ports']=tmp
		if len(self.volumes)>0:
			tmp={}
			volumes=self.volumes.split(",")
			path = self.getBaseDir()
			for volume in volumes:
				if ":" in volume:
					v =volume.split(":")
					if v[0].startswith(path):
						v[0]=v[0][len(path)+1:]
					tmp[v[1]]={"value":v[0],"key":v[1]}
			params['volumes']=tmp
		if len(self.links)>0:
			tmp={}
			links=self.links.split(",")
			for link in links:
				if ":" in link:
					l =link.split(":")
					l_c = Container.objects.filter(name=l[0])
					if(l_c[0]):
						tmp[l[1]]={"value":l[0],"key":l[1],"id":l_c[0].id}
			params['links']=tmp
		if len(self.envs)>0:
			tmp={}
			envs=self.envs.split(",")
			for env in envs:
				if "=" in env:
					e =env.split("=")
					tmp[e[0]]={"key":e[0],"value":e[1]}
			params['envs']=tmp
		return params

	def getBaseDir(self):
		path = files.getUploadDir(str(self.user))
		path = os.path.join(path,'containers',self.name)
		return path

	def getDetailStatus(self):
		result={}
		if self.status==Container.CREATING:
			image = self.image
			result= image.getDetailStatus()
		elif self.status==Container.ERROR:
			result["code"]=-1
			result["detail"]="error"
		else:
			result["code"]=0
			result["detail"]="existed"
		return result
	def getHostConfig(self):
		host_config={}
		if len(self.volumes)>0:
			host_config['Binds']=self.volumes.split(",")
		if len(self.links)>0:
			host_config['Links'] = self.links.split(",")
		if len(self.ports)>0:
			ports = self.ports.split(",")
			port_bind={}
			for p in ports:
				if ":" in p:
					ex = p[0:len(p)-1]+"/tcp"
					de = getPort()
					port_bind[ex]=[{"HostPort":str(de)}]
			host_config['PortBindings']=port_bind
		if self.restart:
			host_config["RestartPolicy"] = { "Name": "always" }
		else:
			host_config["RestartPolicy"] = { "Name": "", "MaximumRetryCount": 5 }
		return host_config
	def getCreateParams(self):
		params={"name":self.name,"image":str(self.image),
			"host_config":self.getHostConfig(),"detach":True}
		if len(self.command)>0:
			params["command"]=self.command.split(",")
		if len(self.envs)>0:
			params["environment"]=self.envs.split(",")
		if len(self.ports)>0:
			ports=self.ports
			ports = ports.replace(":","")
			params['ports']=ports.split(",")
		return params

class Progress(models.Model):
	pid = models.CharField(max_length = 12)
	status = models.CharField(max_length = 100)
	image = models.ForeignKey(Image,on_delete=models.CASCADE,
		related_name="progresses",related_query_name="progress")
	detail = models.CharField(blank=True,max_length = 150)
	pr = models.CharField(blank=True,max_length = 150)
	class Meta:
		unique_together=('pid','image')


	def __unicode__(self):
		return self.id
	def getDetail(self):
		result={}
		if len(self.detail)>0:

			result=json.loads(self.detail)
		return result


def getPort():
	pscmd = "netstat -ntl |grep -v Active| grep -v Proto|awk '{print $4}'|awk -F: '{print $NF}'"
	procs = os.popen(pscmd).read()
	procarr = procs.split("\n")
	tt= random.randint(10000,65534)
	if tt not in procarr:
		return tt
	else:
		getPort()