# -*- coding: UTF-8 -*- 
from django.shortcuts import get_object_or_404,redirect

# Create your views here.
from django.contrib.auth.models import User
from django.contrib import auth
from collections import OrderedDict
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser,MultiPartParser
from rest_framework.decorators import permission_classes,detail_route,list_route
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.reverse import reverse
from .serializers import UserSerializer,ContainerSerializer,ImageSerializer,ProgressSerializer
from .docker_client import DockerClient,DockerHub
from .models import Container,Image,Progress
from api import files
from docker import errors
from mysite import settings
import os,json,markdown,time

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination

    @list_route(methods=['POST'],permission_classes=[AllowAny,])
    def sign_in(self, request):
        data = request.data
        # print(data)
        user = auth.authenticate(username=data['username'],password = data['password'])
        if user and user.is_active:
            auth.login(request,user)
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        return Response("用户名或密码错误",status=404)

    @list_route(methods=['POST'],permission_classes=[AllowAny,])
    def sign_up(self, request):
        data = request.data
        username = data['username']
        email = data['email']
        password = data['password']
        nameFilter = User.objects.filter(username=username)
        emailFilter = User.objects.filter(email=email)
        if(nameFilter):
            return Response("用户名已存在",status=406)
        if(emailFilter):
            return Response("邮箱已注册",status=406)

        # 创建用户
        newUser = User(**data)
        newUser.set_password(password)
        newUser.save()
        # 登陆
        user = auth.authenticate(username=username,password = password)
        if user and user.is_active:
            auth.login(request,user)
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        return Response("验证出错",status=404)

    @list_route()
    def log_out(self, request):
        auth.logout(request)
        return Response("ok")

    @list_route()
    def get_user(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    # @permission_classes(IsAuthenticated)
    # def list(self,request):
    #     pass
class ContainerViewSet(viewsets.ViewSet):

    queryset = Container.objects.all().order_by('-created')
    serializer_class = ContainerSerializer
    pagination_class = StandardResultsSetPagination

    def list(self, request):
        pagination = self.pagination_class()

        queryset = Container.objects.filter(user=request.user)

        data = pagination.paginate_queryset(queryset,request)

        serializer = ContainerSerializer(data,many=True,context={'request': request})
        containers = serializer.data
        cli = DockerClient().getClient()
        for container in containers:
            if container["status"]["code"]==0:
                try:
                    c = cli.inspect_container(container["name"])["State"]["Status"]
                except errors.NotFound:
                    container["status"]["detail"] = "no instance"
                else:
                    container["status"]["detail"] = c
            container["actions"]=self.__actions(container["status"],container["id"],request)
        return pagination.get_paginated_response(containers)

    def retrieve(self, request, pk=None):
        # queryset = Container.objects.all()
        data = get_object_or_404(self.queryset, pk=pk,user=request.user)
        # print self.get_serializer(data).data
        cli = DockerClient().getClient()
        container = {
            "id":data.id,
            "name":data.name,
            "status":data.getDetailStatus(),
            "config":data.getFullConfig(),
            "created":data.created
        }
        if container["status"]["code"]==0:
            try:
                container["inspect"] = cli.inspect_container(data.name)
            except errors.NotFound:
                pass
            else:
                container["status"]["detail"] = container["inspect"]["State"]["Status"]
        container["actions"]=self.__actions(container["status"],container["id"],request)
        return Response(container)

    def __actions(self,status,pk=None,request=None):
        actions=OrderedDict({"detail":{
            "name":"detail",
            "url": reverse("container-detail",args=[pk],request=request)
        }})
        action_delete={"name":"delete","url": reverse("container-detail",args=[pk],request=request)}
        if status["code"]==-1:
            pass
        elif status["code"]==0:
            if status["detail"]=="running":
                actions["stop"]={
                    "name":"stop",
                    "url":reverse("container-stop",args=[pk],request=request)
                }
                actions["restart"]={
                    "name":"restart",
                    "url": reverse("container-restart",args=[pk],request=request)
                }
                actions["pause"]={
                    "name":"pause",
                    "url": reverse("container-pause",args=[pk],request=request)
                }
            elif status["detail"]=="paused":
                actions["unpause"]={
                    "name": "unpause",
                    "url": reverse("container-unpause",args=[pk],request=request)
                }
            else:
                actions["start"]={
                    "name":"start",
                    "url": reverse("container-run",args=[pk],request=request)
                }
                actions["delete"]= action_delete
        elif status["code"]==1:
            actions["start"]={
                "name":"create",
                "url": reverse("container-pull-image",args=[pk],request=request)
            }
            actions["delete"]=action_delete
        elif status["code"]==2:
            actions["start"]={
                "name":"recreate",
                "url": reverse("container-pull-image",args=[pk],request=request)
            }
        else:
            actions["start"]={
                "name":"create",
                "url": reverse("container-run",args=[pk],request=request)
            }
            actions["delete"]=action_delete
        return actions

    # def update(self,request,pk=None):
    #     return Response({"detail":"PUT method forbidden"},status=403)
    
    def destroy(self,request,pk=None):
        data = get_object_or_404(self.queryset, pk=pk,user=request.user)
        cli = DockerClient().getClient()
        try:
            cli.remove_container(data.name)
            
        except errors.APIError,e:
            if e.response.status_code==404:
                pass
            else:
                return Response({"reason":e.response.reason,
                    "detail":e.explanation},status=e.response.status_code)
        v_dir = files.getUploadDir(str(request.user))
        v_dir = os.path.join(v_dir,data.name)
        data.delete()
        files.removeDirs(v_dir)

        
        return Response(ContainerSerializer(data,context={'request':request}).data)

    def create(self,request):
        data = request.data
        nameFilter = Container.objects.filter(name=data.get('name'))     
        # if nameFilter:
        #     return Response("容器名已存在",status=406)
        user = request.user
        data['user'] = user.id
        if data.get('volumes'):
            data['volumes'] = files.resolveVolumes(volumes=data.get('volumes'),path=str(user),name=data.get('name'))
        serializer = ContainerSerializer(data=data)
        if serializer.is_valid():
            valid_data = serializer.data
            valid_data['user'] = user
            #符合条件必定有repo
            repo = valid_data.get('image')
            repos = repo.split(":")
            image_name = repos[0]
            image_tag = "latest"
            if len(repos)==2:
                image_tag = repos[1]
            image = Image.objects.get_or_create(name=image_name,tag=image_tag)[0]
            users =  image.users.filter(pk=user.id)
            if user not in users:
                add = image.users.add(user)
                # image_user=image.users.filter(pk=user.id)
                # print image_user
            valid_data['image']=image
            container = Container(**valid_data)
            container.save()
            #创建成功，返回container
            data=ContainerSerializer(container,context={'request':request}).data
            res = Response(data)
        else:
            res = Response(serializer.errors,status=406)
        return res
    @list_route()
    def names(self,request):
        queryset = Container.objects.filter(user=request.user)
        data=[]
        for c in queryset:
            if c.getDetailStatus().get("code")==0:
                data.append(c.name)
        return Response(data)

    @detail_route()
    def progress(self,request,pk=None):
        container = get_object_or_404(self.queryset, pk=pk,user=request.user)
        # cli = DockerClient().getClient()
        # data = self.get_serializer(container).data
        # data = "To Run"
        if container.getDetailStatus().get("code")==2:
            image = container.image
            progresses = image.progresses.all()
            serializer = ProgressSerializer(progresses,many=True)
            return Response(serializer.data)
        return Response("OK")
    @detail_route()
    def pull_image(self,request,pk=None):
        container = get_object_or_404(self.queryset, pk=pk,user=request.user)
        st = container.getDetailStatus()
        if st['code']==1 or st['code']==2:
            image = container.image
            # 拉取镜像
            image.status = Image.PULLING
            image.save()
            ps = image.progresses.all().delete()
            try:
                cli = DockerClient().getClient()
                pull_image = cli.pull(str(image),stream=True)
                
                for line in pull_image:
                    pr = json.loads(line)
                    status = pr.get("status","")
                    p_id=pr.get("id","")
                    print json.dumps(pr,indent=4)
                    #保存状态
                    if "Pulling from" not in status and len(p_id)==12:
                        progress = Progress.objects.get_or_create(image=image,pid=p_id)[0]
                        progress.status=status
                        detail = pr.get("progressDetail")
                        if detail:
                            progress.detail=json.dumps(detail)
                            progress.pr = pr.get("progress")
                        progress.save()
                if "Status: Downloaded newer image" in status:
                    image.status=Image.EXISTED
                    image.save()
                    ps = image.progresses.all().delete()
                else:
                    image.status=Image.CREATING
                    image.save()
                    return Response({"detail":"Error occurs when pulling image"},status=408)
            except errors.APIError,e:
                image.status=Image.ERROR
                image.save()
                return Response({"reason":e.response.reason,
                    "detail":e.explanation},status=e.response.status_code)
            # print image.status
            # return Response("/api/containers/"+pk+"/progress",status=307)
        #镜像拉取结束后重定向启动应用
        return redirect(reverse('container-run',args=[pk],request=request))

    @detail_route()
    def run(self,request,pk=None):
        container = get_object_or_404(self.queryset, pk=pk,user=request.user)
        cli = DockerClient().getClient()
        data={}
        st = container.getDetailStatus()
        try:
            if st['code']==3:
                params = container.getCreateParams()
                data = cli.create_container(**params)
                if data.get("Id"):
                    container.status=Container.EXISTED
                    container.save()
                    cli.start(container.name)
                    return Response(True)
            elif st['code']==0:
                cli.start(container.name)
                return Response(True)
            elif st['code']==1 or st['code']==2:
                return redirect(reverse('container-progress',args=[pk],request=request))
        except errors.APIError,e:
            if e.response.status_code==404:
                image=container.image
                image.status=Image.CREATING
                image.save()

            return Response({"reason":e.response.reason,
                    "detail":e.explanation},status=e.response.status_code)
        # 应用状态出错，不能启动
        # print data
        return Response(False)

    @detail_route()
    def stop(self,request,pk=None):
        container = get_object_or_404(self.queryset, pk=pk,user=request.user)
        cli = DockerClient().getClient()
        st = container.getDetailStatus()
        data = ContainerSerializer(container,context={'request':request}).data
        if st['code']==0:
            try:
                data=cli.stop(container.name)
            except errors.APIError,e:
                return Response({"reason":e.response.reason,
                    "detail":e.explanation},status=e.response.status_code)
        # print data
        return Response(data)
    @detail_route()
    def restart(self,request,pk=None):
        container = get_object_or_404(self.queryset, pk=pk,user=request.user)
        cli = DockerClient().getClient()
        st = container.getDetailStatus()
        data = ContainerSerializer(container,context={'request':request}).data
        if st['code']==0:
            try:
                data=cli.restart(container.name)
            except errors.APIError,e:
                return Response({"reason":e.response.reason,
                    "detail":e.explanation},status=e.response.status_code)
        # print data
        return Response(data)
    @detail_route()
    def pause(self,request,pk=None):
        container = get_object_or_404(self.queryset, pk=pk,user=request.user)
        cli = DockerClient().getClient()
        st = container.getDetailStatus()
        data = ContainerSerializer(container,context={'request':request}).data
        if st['code']==0:
            try:
                data=cli.pause(container.name)
            except errors.APIError,e:
                return Response({"reason":e.response.reason,
                    "detail":e.explanation},status=e.response.status_code)
        # print data
        return Response(data)
    @detail_route()
    def unpause(self,request,pk=None):
        container = get_object_or_404(self.queryset, pk=pk,user=request.user)
        cli = DockerClient().getClient()
        st = container.getDetailStatus()
        data = ContainerSerializer(container,context={'request':request}).data
        if st['code']==0:
            try:
                data=cli.unpause(container.name)
            except errors.APIError,e:
                return Response({"reason":e.response.reason,
                    "detail":e.explanation},status=e.response.status_code)
        # print data
        return Response(data)

class RepoViewSet(viewsets.ViewSet):
    def list(self,request):
        base_url = "http://"+request.get_host()+request.path
        cli  = DockerHub()
        query = request.query_params.get("query")
        if query:
            data=cli.searchRepo(request.query_params)
        else:

            namespace = request.query_params.get("namespace")
            data = cli.getRepoList(namespace,request.query_params)

        r_previous = data.get('previous')
        r_next = data.get('next')
        if r_previous:
            pages=r_previous.split("?")
            data['previous'] = base_url+"?"+pages[1]
        if r_next:
            pages = r_next.split("?")
            data['next'] = base_url+"?"+pages[1]

        return Response(OrderedDict([
            ("count",data.get('count')),
            ("next",data.get('next')),
            ("previous",data.get('previous')),
            ("results",data.get('results'))]))

    def retrieve(self,request,pk=None):
        cli  = DockerHub()
        namespace = request.query_params.get("namespace")
        data=cli.getRepoDetail(pk,namespace)
        mk = data.get("full_description")
        if mk:
            data['full_description'] = markdown.markdown(mk,extensions=['markdown.extensions.tables','markdown.extensions.fenced_code'])
        else:
            return Response(data,status=404)
        return Response(data)

    @detail_route()
    def tags(self,request,pk=None):
        base_url = "http://"+request.get_host()+request.path
        cli = DockerHub()
        namespace = request.query_params.get("namespace")
        tag_name = request.query_params.get("name")
        # params={}
        # params['page']=request.query_params.get("page",1)
        # params['page_size'] = request.query_params.get('page_size')
        data=cli.getRepoTags(pk,namespace,tag_name,request.query_params)
        r_previous = data.get('previous')
        r_next = data.get('next')
        if r_previous:
            pages=r_previous.split("?")
            data['previous'] = base_url+"?"+pages[1]
        if r_next:
            pages = r_next.split("?")
            data['next'] = base_url+"?"+pages[1]
        return Response(OrderedDict([
            ("count",data.get('count')),
            ("next",data.get('next')),
            ("previous",data.get('previous')),
            ("results",data.get('results'))]))


class ImageViewSet(viewsets.ModelViewSet):

    queryset = Image.objects.all().order_by('-created')
    serializer_class = ImageSerializer
    pagination_class = StandardResultsSetPagination

    # def list(self, request):
        
    #     cli = DockerClient().getClient()
    #     try:
    #         images = cli.images()
    #     except errors.NotFound:
    #         pass
    #     else:
    #         return Response(images)

    # def retrieve(self, request, pk=None):
    #     cli = DockerClient().getClient()
    #     try:
    #         image = cli.inspect_image(pk)
    #     except errors.NotFound:
    #         return Response({"detail":"Not found."},status=404)
    #     else:
    #         return Response(image)

class FileViewSet(viewsets.ViewSet):
    def list(self,request):
        # path = request.query_params.get("path")
        # if path:
        #     path = request.user.username+"/"+path
        # else:
        #     path = request.user.username
        file_list = files.fileList(request.user.username)
        if file_list:
            return Response(file_list)
        return Response(status=404);

    # 上传文件
    def create(self, request,format=None):
        file_obj = request.data['file']
        status = files.fileUpload(str(file_obj),file_obj,request.user.username)
        
        # ...
        # do some stuff with uploaded file
        # ...
        return Response(status=status)
    @list_route()
    def rename(self,request):
        user = request.user;
        path=files.getUploadDir(str(user))
        # print request.query_params
        filename=request.query_params.get("filename","")
        newname = request.query_params.get("newname","")
        # print filename,newname
        if len(filename) and len(newname):
            filename=os.path.join(path,filename)
            newname=os.path.join(path,newname)
            return Response(status=files.renameFile(filename,newname))
        return Response({"detail":"filename and newname required"},status=406)
    @list_route()
    def remove(self,request):
        path = files.getUploadDir(str(request.user))
        filename = request.query_params.get("filename","")
        if len(filename):
            filename=os.path.join(path,filename)
            return Response(status=files.destroyFile(filename))
        return Response({"detail":"filename required"},status=406)