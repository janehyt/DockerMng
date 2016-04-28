# -*- coding: UTF-8 -*- 
from docker import Client
from mysite import settings as settings
import json
import requests

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

class DockerHub(object):
	__metaclass__=Singleton

	_host = "hub.docker.com"
	# _base_url= "https://"+_host+"/v2/repostories"
	_offical = "library"
	def __init__(self,host=None):
		if host:
			self._host=host
		self._base_url="https://"+self._host+"/v2/repositories"


	def getRepo(self,namespace,page='1'):
		r = requests.get(self._base_url+"/"+namespace+"/?page="+page)
		result = json.loads(r.text)
			
		return result

	def getOfficalRepo(self,page='1'):
		return self.getRepo(self._offical,page)

	def getImage(self,namespace,name):
		r = requests.get(self._base_url+"/"+namespace+"/"+name)
		result = json.loads(r.text)
		return result

	def getOfficalImage(self,name):
		return self.getImage(self._offical,name)	