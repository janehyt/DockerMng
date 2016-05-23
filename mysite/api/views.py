# -*- coding: UTF-8 -*- 
from django.shortcuts import get_object_or_404,redirect

# Create your views here.
from django.contrib.auth.models import User
from django.contrib import auth

from collections import OrderedDict
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import permission_classes,detail_route,list_route
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.reverse import reverse
from django.http import StreamingHttpResponse
from docker import errors

from .serializers import UserSerializer,ImageSerializer,RepoSerializer,ProcessSerializer
from .files import VolumeService
from .dockerconn import DockerHub,DockerClient
from .models import Image,Repository,Process
import markdown,json

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
        user = auth.authenticate(username=data.get('username'),password = data.get('password'))
        if user and user.is_active:
            auth.login(request,user)
            serializer = self.get_serializer(user)
            # to = Token.objects.get_or_create(user=user)
            # print to
            return Response(serializer.data)
        validation_error="请输入正确的用户名和密码."
        return Response(validation_error,status=400)

    @list_route(methods=['POST'],permission_classes=[AllowAny,])
    def sign_up(self, request):
        data = request.data

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return self.sign_in(request)
        errors = ""
        if "username" in serializer.errors:
            errors = "用户名已存在,"
        if "email" in serializer.errors:
            errors+="邮箱已被注册,"
        return Response(errors[0:len(errors)-1],status=400)

    @list_route(methods=['POST'])
    def reset(self, request):
        data = request.data
        user = request.user
        oldpass = data['oldpass']
        password = data['password']
        if auth.authenticate(username=user.username,password = oldpass):
            user.set_password(password)
            user.save()
            return Response(True)
        return Response("原密码错误",status=400)
    @list_route(methods=['POST'])
    def log_out(self, request):
        m=auth.logout(request)
        return Response(m)

    @list_route()
    def load_user(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class ImageViewSet(viewsets.ModelViewSet):

    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    pagination_class = StandardResultsSetPagination

    def list(self, request):
        pagination = self.pagination_class()
        query = request.query_params.get("query","")
        queryset = Image.objects.filter(users=request.user,repository__contains=query)

        data = pagination.paginate_queryset(queryset,request)

        serializer = ImageSerializer(data,many=True,context={'request': request})
        images = serializer.data
        
        return pagination.get_paginated_response(images)

    @list_route(methods=['POST'])
    def pull(self, request):
        data = request.data
        repository = data.get("repository","")
        tag = data.get("tag","")
        user = request.user
        if repository and tag:
            image = Image.objects.get_or_create(repository=repository,tag=tag)[0]
            users =  image.users.filter(pk=user.id)
            if user not in users:
                add = image.users.add(user)
                image.save()
            if not image.isbuild:
                image.status=Image.PULLING
                image.save()
                ps = image.processes.all().delete()
                try:
                    cli = DockerClient().getClient()
                    pull_image = cli.pull(unicode(image),stream=True)
                    for line in pull_image:
                        pr = json.loads(line)
                        status = pr.get("status","")
                        p_id = pr.get("id",Process.DEFAULT)
                        # if "Pulling from" not in status:
                        process = Process.objects.get_or_create(image=image,pid=p_id)[0]
                        process.status=status
                        detail = pr.get("progressDetail",{})
                        process.detail=json.dumps(detail)
                        process.pr = pr.get("progress","")
                        process.save()
                    if "Status: Downloaded newer image" in status or "Status: Image is up to date" in status:
                        image.status=Image.EXISTED
                        image.save()
                        ps = image.processes.all().delete()
                    else:
                        image.status=Image.ERROR
                        image.save()
                        return Response({"detail":"Error occurs when pulling image"},status=408)
                except errors.APIError,e:
                    image.status=Image.ERROR
                    image.save()
                    return Response({"reason":e.response.reason,
                        "detail":e.explanation},status=e.response.status_code)

            return Response(ImageSerializer(image).data)
        else:
            return Response({"detail":"请提供repository和tag"},status=400)

    @list_route(methods=['POST'])
    def build(self, request):
        data = request.data
        user = request.user
        repository = data.get("repository","")
        tag = data.get("tag","")
        builddir = VolumeService(user,data.get("builddir","")).getPath()
       
        
        repository.split("/")

        if repository and tag and builddir and repository.find(Repository.LOCAL+"/") is 0:
            re = Repository.objects.filter(namespace=Repository.LOCAL,name=repository.split("/")[1])
            if len(re) is 1:
                data["builddir"]=builddir
                data["isbuild"]=True
                data["status"]=Image.BUILDING
                serializer = ImageSerializer(data=data)
                if serializer.is_valid():
                    image = serializer.save()
                    image.users.add(user)
                    image.save()
                    return Response(serializer.data)
                else:
                    return Response("该仓库下已存在该标签构建的镜像",status=400)
            else:
               pass
        return Response("请给出合适的repository、tag、path",status=400)

    @detail_route()
    def process(self,request,pk=None):
        image = get_object_or_404(self.queryset, pk=pk,users=request.user)
        
        if image.status == Image.PULLING or image.status==Image.BUILDING:
            processes = image.processes.all()
            # print type(processes)
            serializer = ProcessSerializer(processes,many=True)
            # print serializer.data
            return Response(serializer.data)
        return Response("OK")

class RepoViewSet(viewsets.ModelViewSet):

    queryset = Repository.objects.all()
    serializer_class = RepoSerializer
    pagination_class = StandardResultsSetPagination

    def list(self,request):
        
        query = request.query_params.get("query","")
        namespace = request.query_params.get("namespace","library")

        if namespace==Repository.LOCAL:
            pagination = self.pagination_class()
            
            queryset = Repository.objects.filter(user=request.user,name__contains=query)

            data = pagination.paginate_queryset(queryset,request)

            serializer = RepoSerializer(data,many=True)
            repos = serializer.data
            
            return pagination.get_paginated_response(repos)

        base_url = "http://"+request.get_host()+request.path
        cli  = DockerHub()
        if query:
            data=cli.searchRepo(request.query_params)
            
        else:
            # namespace = request.query_params.get("namespace")
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
        
        namespace = request.query_params.get("namespace","library")
        if namespace==Repository.LOCAL:
            data = get_object_or_404(self.queryset, name=pk,user=request.user)
            re = RepoSerializer(data).data
            re["full_description"]=markdown.markdown(data.description,extensions=['markdown.extensions.tables','markdown.extensions.fenced_code'])
            return Response(re)
        
        cli  = DockerHub()
        data=cli.getRepoDetail(pk,namespace)
        mk = data.get("full_description")
        if mk:
            data['full_description'] = markdown.markdown(mk,extensions=['markdown.extensions.tables','markdown.extensions.fenced_code'])
        else:
            return Response(data,status=404)
        return Response(data)

    def create(self,request):
        data = request.data
        data["namespace"] = Repository.LOCAL
        data["user"]=request.user.id
        serializer = RepoSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.save())
    @detail_route()
    def tags(self,request,pk=None):
        namespace = request.query_params.get("namespace","library")
        tag_name = request.query_params.get("name","")

        if namespace==Repository.LOCAL:
            queryset = Image.objects.filter(repository=namespace+"/"+pk,tag__contains=tag_name)
            pagination = StandardResultsSetPagination()
            data = pagination.paginate_queryset(queryset,request)

            return pagination.get_paginated_response(ImageSerializer(data,many=True).data)

        base_url = "http://"+request.get_host()+request.path
        cli = DockerHub()
        
        
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

class VolumeViewSet(viewsets.ViewSet):
    def list(self,request):
        path = request.query_params.get("path","")
        files = VolumeService(request.user,path)
        data = files.list()
        if data is None:
            return Response({"detail":"找不到指定路径"},status = 404)
        return Response(data);
    @list_route()
    def download(self,request):
        path = request.query_params.get("path","")
        files = VolumeService(request.user,path)
        data = files.download()
        if data is None:
            return Response({"detail":"找不到指定路径"},status = 404)
        response = StreamingHttpResponse(data.get("stream"))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(data.get("name"))
        return response

    # 上传文件
    def create(self, request,format=None):
        file_obj = request.data['file']
        path = request.query_params.get("path","")
        files = VolumeService(request.user,path)
        status = files.fileUpload(str(file_obj),file_obj)
        return Response(status=status)

    @list_route(methods=['POST'])
    def rename(self,request):
        path = request.data.get("path","")
        name = request.data.get("name","")
        if path and name:    
            files = VolumeService(request.user,path)
            return Response(files.rename(name))
        return Response({"detail":"请提供path和name"},status=400)

    @list_route(methods=['POST'])
    def remove(self,request):
        path = request.data.get("path","")
        # name = request.data.get("name","")
        if path: 
            files = VolumeService(request.user,path)
            return Response(files.remove())
        return Response({"detail":"请提供path"},status=400)

    @list_route(methods=['POST'])
    def mkdir(self,request):
        path = request.data.get("path","")
        name = request.data.get("name","")
        if name:    
            files = VolumeService(request.user,path)
            return Response(status=files.mkdir(name))
        return Response({"detail":"请提供path和name"},status=400)

    @list_route(methods=['POST'])
    def unzip(self,request):
        path = request.data.get("path","")       
        if path:    
            files = VolumeService(request.user,path)
            return Response(status=files.unzip())
        return Response({"detail":"请提供path"},status=400)