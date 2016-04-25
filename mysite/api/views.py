# -*- coding: UTF-8 -*- 
from django.shortcuts import render,get_object_or_404

# Create your views here.
from django.contrib.auth.models import User
from rest_framework import viewsets
from api.serializers import UserSerializer,ContainerSerializer
from rest_framework.response import Response
from rest_framework.decorators import permission_classes,detail_route,list_route
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib import auth
from api.docker_client import DockerClient
from .models import Container
import time
from docker import errors



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # permission_classes = (AllowAny,)

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
        queryset = Container.objects.filter(user=request.user)
        serializer = ContainerSerializer(queryset,many=True)
        containers = serializer.data
        cli = DockerClient().getClient()
        for container in containers:
            try:
                c = cli.inspect_container(container["name"])["State"]
            except errors.NotFound:
                container["state"] = {"Status":"ghost"}
            else:
                print container["name"]
                container["state"] = c

        # for container in queryset:
        #     print(container)
        return Response(containers)

    def retrieve(self, request, pk=None):
        # queryset = Container.objects.all()
        data = get_object_or_404(self.queryset, pk=pk,user=request.user)
        cli = DockerClient().getClient()
        try:
            container = cli.inspect_container(data.name)
        except errors.NotFound:
            return Response({"detail":"Not found."},status=404)
        else:    
            return Response(container)

    def perform_create(self, serializer):
        print(self.request.data)
        serializer.save(user=self.request.user)