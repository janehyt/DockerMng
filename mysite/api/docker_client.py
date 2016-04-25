# -*- coding: UTF-8 -*- 
from docker import Client
from mysite import settings as settings
import json

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