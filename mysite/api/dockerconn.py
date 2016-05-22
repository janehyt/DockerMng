from docker import Client
from mysite import settings as settings
import json,requests
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
		for repo in result.get("results"):
			fullname = repo.get("repo_name").split("/")
			if(len(fullname)==2):
				repo["namespace"]=fullname[0]
				repo["name"]=fullname[1]
			else:
				repo["namespace"]=self._offical
				repo["name"]=fullname[0]


		return result