# -*- coding: UTF-8 -*- 
from django.shortcuts import get_object_or_404

# Create your views here.
from django.contrib.auth.models import User
from django.contrib import auth
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import permission_classes,detail_route,list_route
from rest_framework.permissions import AllowAny,IsAuthenticated
from .serializers import UserSerializer,ContainerSerializer,ImageSerializer
from .docker_client import DockerClient,DockerHub
from .models import Container,Image
import time
from docker import errors
import markdown


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

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
class ContainerViewSet(viewsets.ModelViewSet):

    queryset = Container.objects.all().order_by('-created')
    serializer_class = ContainerSerializer

    def list(self, request):
        # cli = DockerClient().getClient()
        # containers = cli.containers(all=1)
        base_url = "http://"+request.get_host()+request.path
        count= Container.objects.filter(user=request.user).count()

        page = request.query_params.get('page')
        size = 3
        if not page:
            page='1'
        
        if not page.isdigit():
            return Response({'detail':'Invalid page.'},status=404)
        page = int(page)

        if page==0 or (page-1)*size>=count:
             return Response({'detail':'Invalid page.'},status=404)

        queryset = Container.objects.filter(user=request.user)[(page-1)*size:page*size]
        
        serializer = ContainerSerializer(queryset,many=True,context={'request': request})
        containers = serializer.data
        cli = DockerClient().getClient()
        for container in containers:
            try:
                c = cli.inspect_container(container["name"])["State"]
            except errors.NotFound:
                container["state"] = {"Status":"ghost"}
            else:
                container["state"] = c
                container["url"] = base_url+str(container['id'])
        # for container in queryset:
        #     print(container)
        r_previous = None
        if page-1>0:
            r_previous = base_url+"?page="+str(page-1)
        r_next = None
        if page*size<count:
            r_next = base_url+"?page="+str(page+1)
        data={"count":count,
            "previous": r_previous,
            "next": r_next,
            "results":containers
        }
        return Response(data)

    def retrieve(self, request, pk=None):
        # queryset = Container.objects.all()
        data = get_object_or_404(self.queryset, pk=pk,user=request.user)
        cli = DockerClient().getClient()
        try:
            container = cli.inspect_container(data.name)
        except errors.NotFound:
            return Response({"detail":"Not found."},status=404)
        else: 
            container['url'] = "http://"+request.get_host()+request.path
            return Response(container)

class ImageViewSet(viewsets.ViewSet):

    def list(self, request):
        
        cli = DockerClient().getClient()
        try:
            images = cli.images()
        except errors.NotFound:
            pass
        else:
            return Response(images)

    def retrieve(self, request, pk=None):
        cli = DockerClient().getClient()
        try:
            image = cli.inspect_image(pk)
        except errors.NotFound:
            return Response({"detail":"Not found."},status=404)
        else:
            return Response(image)
        

    @list_route()    
    def officialRepos(self,request):
        base_url = "http://"+request.get_host()+request.path
        cli  = DockerHub()
        data={}

        name = request.query_params.get('name')
        if name:
            data=cli.getOfficalImage(name)
            data['full_description'] = markdown.markdown(data['full_description'])
        else:

            page = request.query_params.get('page')
            if not page:
                page = '1'
            
            data = cli.getOfficalRepo(page)

            r_previous = data.get('previous')
            r_next = data.get('next')
            if r_previous:
                pages=r_previous.split("?")
                data['previous'] = base_url+"?"+pages[1]
            if r_next:
                pages = r_next.split("?")
                data['next'] = base_url+"?"+pages[1]

        return Response(data)

    @list_route()    
    def officialImage(self,request):
        base_url = "http://"+request.get_host()+request.path

        page = request.query_params.get('page')
        if not page:
            page = '1'
        cli  = DockerHub()
        data = cli.getOfficalRepo(page)

        r_previous = data.get('previous')
        r_next = data.get('next')
        if r_previous:
            pages=r_previous.split("?")
            data['previous'] = base_url+"?"+pages[1]
        if r_next:
            pages = r_next.split("?")
            data['next'] = base_url+"?"+pages[1]

        return Response(data)
        
    # def perform_create(self, serializer):
    #     print(self.request.data)
    #     serializer.save(user=self.request.user)