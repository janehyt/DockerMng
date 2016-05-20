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
from .serializers import UserSerializer


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
            # user = auth.authenticate(username=user.username,password = password)
            # auth.login(request,user)
            # print user.is_active
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