'''dockerconn'''
# -*- coding: UTF-8 -*-
import json
import requests
from docker import Client
from mysite import settings as settings

# class Singleton(type):
#     '''Singleton'''
#     def __init__(cls, name, bases, dic):
#         super(Singleton, cls).__init__(name, bases, dic)
#         cls._instance = None
#     def __call__(cls, *args, **kw):
#         if cls._instance is None:
#             cls._instance = super(Singleton, cls).__call__(*args, **kw)
#         return cls._instance

class DockerClient(object):
    '''DockerClient'''
    # __metaclass__ = Singleton
    def __init__(self, url=settings.DOCKER_CLIENT):
        self.__url = url
        self.__client = Client(base_url=url)

    def get_client(self):
        '''get_client'''
        return self.__client

class DockerHub(object):
    '''DockerHub'''
    # __metaclass__ = Singleton
    __host = "hub.docker.com"
    # _base_url= "https://"+_host+"/v2/repostories"
    __offical = "library"
    def __init__(self, host=None):
        if host:
            self.__host = host
        self.__base_url = "https://"+self.__host+"/v2/repositories"
        self.__search_url = "https://"+self.__host+"/v2/search/repositories/"

    def get_repo_list(self, namespace=None, params=None):
        '''get_repo_list'''
        if not namespace:
            namespace = self.__offical
        response = requests.get(self.__base_url+"/"+namespace, params)
        result = json.loads(response.text)
        return result

    def get_repo_detail(self, name, namespace=None):
        '''get_repo_detail'''
        if not namespace:
            namespace = self.__offical
        response = requests.get(self.__base_url+"/"+namespace+"/"+name)
        result = json.loads(response.text)
        return result

    def get_repo_tags(self, name, namespace=None, tag_name=None, params=None):
        '''get_repo_tags'''
        if not namespace:
            namespace = self.__offical
        if not tag_name:
            tag_name = ""
        response = requests.get(self.__base_url+"/"+namespace+"/"+name+"/tags/"+tag_name, params)
        result = json.loads(response.text)
        return result

    def search_repo(self, params=None):
        '''search_repo'''
        response = requests.get(self.__search_url, params)
        result = json.loads(response.text)
        for repo in result.get("results"):
            fullname = repo.get("repo_name").split("/")
            if len(fullname) == 2:
                repo["namespace"] = fullname[0]
                repo["name"] = fullname[1]
            else:
                repo["namespace"] = self.__offical
                repo["name"] = fullname[0]
        return result
