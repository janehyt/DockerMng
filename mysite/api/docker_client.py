# -*- coding: UTF-8 -*- 
from docker import Client
from mysite import settings as settings
import json
import requests
import os
import random

class Singleton(type):  
    def __init__(cls, name, bases, dict):    
        super(Singleton, cls).__init__(name, bases, dict)    
        cls._instance = None    
    def __call__(cls, *args, **kw):    
        if cls._instance is None:    
            cls._instance = super(Singleton, cls).__call__(*args, **kw)    
        return cls._instance 

class DockerClient(object):

	__metaclass__ = Singleton

	def __init__(self,url = settings.DOCKER_CLIENT):
		self.client = Client(base_url = url)


	def getClient(self):
		return self.client

	def getInfo(self): 
		return 	json.dumps(self.client.info())

	def getHostConfig(self,volumes="",links="",ports="",restart=False):
		host_config={}
		if len(volumes)>0:
			host_config['Binds']=volumes.split(",")
		if len(links)>0:
			host_config['Links'] = links.split(",")
		if len(ports)>0:
			ports = ports.split(",")
			port_bind={}
			for p in ports:
				if ":" in p:
					ex = p[0:len(p)-1]+"/tcp"
					de = getPort()
					port_bind[ex]=[{"HostPort":str(de)}]
			host_config['PortBindings']=port_bind
		if restart:
			host_config["RestartPolicy"] = { "Name": "always" }
		else:
			host_config["RestartPolicy"] = { "Name": "", "MaximumRetryCount": 5 }
		return host_config

class DockerHub(object):
	__metaclass__=Singleton

	_host = "hub.docker.com"
	# _base_url= "https://"+_host+"/v2/repostories"
	_offical = "library"
	def __init__(self,host=None):
		if host:
			self._host=host
		self._base_url="https://"+self._host+"/v2/repositories"
		self._search_url = "https://"+self._host+"/v2/search/repositories/"


	def getRepoList(self,namespace=None,params={}):
		if not namespace:
			namespace = self._offical
		r = requests.get(self._base_url+"/"+namespace,params)
		result = json.loads(r.text)
			
		return result

	def getRepoDetail(self,name,namespace=None):
		if not namespace:
			namespace = self._offical
		r = requests.get(self._base_url+"/"+namespace+"/"+name)
		result = json.loads(r.text)
		return result

	def getRepoTags(self,name,namespace=None,tag_name=None,params={}):
		if not namespace:
			namespace=self._offical
		if not tag_name:
			tag_name=""
		r = requests.get(self._base_url+"/"+namespace+"/"+name+"/tags/"+tag_name,params)
		result=json.loads(r.text)
		return result
		
	def searchRepo(self,params={}):
		r = requests.get(self._search_url,params)
		result=json.loads(r.text)
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