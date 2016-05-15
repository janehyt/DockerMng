# -*- coding: UTF-8 -*- 
from docker import Client
from mysite import settings as settings
import json
import requests
# import os
# import random

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
	def getStats(self,container=""):
		data={}
		if len(container):
			d = self.client.stats(container=container,stream=False)
			data["block"]=self.__solve_block(d.get("blkio_stats"))
			data["cpu"]=self.__solve_cpu(d.get("cpu_stats"))
			data["memory"]=self.__solve_memory(d.get("memory_stats"))
			data["network"]=self.__solve_net(d.get("networks"))

		return data
	def __solve_block(self,block):
		block_data={"Read":0,"Write":0,"Sync":0,"Async":0,"Total":0}
		tmp = block.get("io_service_bytes_recursive")
		if tmp:	
			for t in tmp:
				if t.get("op") in block_data:
					block_data[t.get("op")]=block_data[t.get("op")]+t.get("value",0)
		return block_data
	def __solve_cpu(self,cpu):
		return {
			"usermode":cpu["cpu_usage"]["usage_in_usermode"],
			"kernelmode":cpu["cpu_usage"]["usage_in_kernelmode"],
			"total":cpu["cpu_usage"]["total_usage"],
			"system":cpu["system_cpu_usage"]
		}
	def __solve_memory(self,memory):
		return {
			"usage":memory["usage"],
			"limit":memory["limit"],
			"max":memory["max_usage"],
		}
	def __solve_net(self,net):
		net_data={"read":0,"write":0}
		if net:
			for n in net:
				net_data["read"]+=net[n]["rx_bytes"]
				net_data["write"]+=net[n]["tx_bytes"]
		return net_data
		



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


