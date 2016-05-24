'''views'''
# -*- coding: UTF-8 -*-
import json
# from collections import OrderedDict
import markdown
from django.shortcuts import get_object_or_404
# Create your views here.
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import StreamingHttpResponse
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import AllowAny
# from rest_framework.reverse import reverse
from docker import errors
from .serializers import UserSerializer, ImageSerializer,\
RepoSerializer, ProcessSerializer
from .files import VolumeService
from .dockerconn import DockerHub, DockerClient
from .models import Image, Repository, Process
from .helper import ImageHelper

class StandardResultsSetPagination(PageNumberPagination):
    """
    Pagination
    """
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

    @list_route(methods=['POST'], permission_classes=[AllowAny,])
    def sign_in(self, request):
        '''sign_in'''
        data = request.data
        user = auth.authenticate(username=data.get('username'),\
            password=data.get('password'))
        if user and user.is_active:
            auth.login(request, user)
            serializer = self.serializer_class(user,context={"request":request})
            # to = Token.objects.get_or_create(user=user)
            # print to
            return Response(serializer.data)
        validation_error = "请输入正确的用户名和密码."
        return Response(validation_error, status=400)

    @list_route(methods=['POST'], permission_classes=[AllowAny,])
    def sign_up(self, request):
        '''sign_up'''
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return self.sign_in(request)
        errormsg = ""
        if "username" in serializer.errors:
            errormsg = "用户名已存在,"
        if "email" in serializer.errors:
            errormsg += "邮箱已被注册,"
        return Response(errormsg[0:len(errormsg)-1], status=400)

    @list_route(methods=['POST'])
    def reset(self, request):
        '''reset'''
        data = request.data
        user = request.user
        oldpass = data['oldpass']
        password = data['password']
        if auth.authenticate(username=user.username, password=oldpass):
            user.set_password(password)
            user.save()

            return Response(self.get_serializer(user).data)
        return Response("原密码错误", status=400)

    @list_route(methods=['POST'])
    def log_out(self, request):
        '''log_out'''
        serializer = self.get_serializer(request.user)
        auth.logout(request)
        return Response(serializer.data)

    @list_route()
    def load_user(self, request):
        '''load_user'''
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class ImageViewSet(viewsets.ModelViewSet):
    '''ImageViewSet'''
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    pagination_class = StandardResultsSetPagination
    helper_class = ImageHelper

    def list(self, request):
        '''list'''
        pagination = self.pagination_class()
        query = request.query_params.get("query", "")
        queryset = Image.objects.filter(users=request.user,\
            repository__contains=query)
        data = pagination.paginate_queryset(queryset, request)
        serializer = ImageSerializer(data, many=True,\
            context={'request': request})
        images = serializer.data
        return pagination.get_paginated_response(images)

    @list_route(methods=['POST'])
    def pull(self, request):
        '''pull'''
        if "repository" in request.data and "tag" in request.data:
            image = Image.objects.get_or_create(\
                repository=request.data.get("repository"),\
                tag=request.data.get("tag"))[0]
            users = image.users.filter(pk=request.user.id)
            if request.user not in users:
                image.users.add(request.user)
                image.save()
            if not image.isbuild:
                status = self.helper_class(image).pull()
                return Response(status)
            return Response(self.serializer_class(image).data)
        else:
            return Response({"detail":"请提供repository和tag"}, status=400)

    @list_route(methods=['POST'])
    def build(self, request):
        '''build'''
        data = request.data
        user = request.user
        repository = data.get("repository", "")
        tag = data.get("tag", "")
        builddir = VolumeService(user, data.get("builddir", "")).get_path()
        repository.split("/")
        if repository and tag and builddir and\
        repository.find(Repository.LOCAL+"/") is 0:
            response = Repository.objects.filter(namespace=Repository.LOCAL,\
                name=repository.split("/")[1])
            if len(response) is 1:
                data["builddir"] = builddir
                data["isbuild"] = True
                data["status"] = Image.BUILDING
                serializer = self.serializer_class(data=data)
                if serializer.is_valid():
                    image = serializer.save()
                    image.users.add(user)
                    image.save()
                    return Response(serializer.data)
                else:
                    return Response("该仓库下已存在该标签构建的镜像", status=400)
            else:
                pass
        return Response("请给出合适的repository、tag、path", status=400)

    @detail_route()
    def process(self, request, pk=None):#pylint: disable=invalid-name
        '''process'''
        image = get_object_or_404(self.queryset, pk=pk, users=request.user)
        if image.status == Image.PULLING or image.status == Image.BUILDING:
            processes = image.processes.all()
            serializer = ProcessSerializer(processes, many=True)
            # print serializer.data
            return Response(serializer.data)
        return Response("OK")

class RepoViewSet(viewsets.ViewSet):
    '''RepoViewSet'''
    queryset = Repository.objects.all()
    serializer_class = RepoSerializer
    pagination_class = StandardResultsSetPagination

    def list(self, request):
        '''list'''
        query = request.query_params.get("query", "")
        namespace = request.query_params.get("namespace", "library")
        if namespace == Repository.LOCAL:
            pagination = self.pagination_class()
            queryset = Repository.objects.filter(user=request.user,\
                name__contains=query)
            data = pagination.paginate_queryset(queryset, request)
            serializer = self.serializer_class(data, many=True)
            repos = serializer.data
            return pagination.get_paginated_response(repos)

        base_url = "http://"+request.get_host()+request.path
        cli = DockerHub()
        if query:
            data = cli.search_repo(request.query_params)
        else:
            # namespace = request.query_params.get("namespace")
            data = cli.get_repo_list(namespace, request.query_params)

        r_previous = data.get('previous')
        r_next = data.get('next')
        if r_previous:
            pages = r_previous.split("?")
            data['previous'] = base_url+"?"+pages[1]
        if r_next:
            pages = r_next.split("?")
            data['next'] = base_url+"?"+pages[1]
        return Response(data)

    def retrieve(self, request, pk=None):#pylint: disable=invalid-name
        '''retrieve'''
        namespace = request.query_params.get("namespace", "library")
        if namespace == Repository.LOCAL:
            data = get_object_or_404(self.queryset, name=pk, user=request.user)
            res = self.serializer_class(data).data
            res["full_description"] = markdown.markdown(data.description,\
                extensions=['markdown.extensions.tables',\
                'markdown.extensions.fenced_code'])
            return Response(res)
        cli = DockerHub()
        data = cli.get_repo_detail(pk, namespace)
        mkd = data.get("full_description")
        if mkd:
            data['full_description'] = markdown.markdown(mkd,\
                extensions=['markdown.extensions.tables',\
                'markdown.extensions.fenced_code'])
        else:
            return Response(data, status=404)
        return Response(data)

    def create(self, request):
        '''create'''
        data = request.data
        data["namespace"] = Repository.LOCAL
        data["user"] = request.user.id
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(self.serializer_class(serializer.save()).data)
    @detail_route()
    def tags(self, request, pk=None):#pylint: disable=invalid-name
        '''tags'''
        namespace = request.query_params.get("namespace", "library")
        tag_name = request.query_params.get("name", "")

        if namespace == Repository.LOCAL:
            queryset = Image.objects.filter(repository=namespace+"/"+pk,\
                tag__contains=tag_name)
            pagination = self.pagination_class()
            data = pagination.paginate_queryset(queryset, request)

            return pagination.get_paginated_response(ImageSerializer(data,\
                many=True).data)

        base_url = "http://"+request.get_host()+request.path
        cli = DockerHub()
        data = cli.get_repo_tags(pk, namespace, tag_name, request.query_params)
        r_previous = data.get('previous')
        r_next = data.get('next')
        if r_previous:
            pages = r_previous.split("?")
            data['previous'] = base_url+"?"+pages[1]
        if r_next:
            pages = r_next.split("?")
            data['next'] = base_url+"?"+pages[1]
        return Response(data)

class VolumeViewSet(viewsets.ViewSet):
    '''VolumeViewSet'''
    service = VolumeService

    def list(self, request):
        '''list'''
        path = request.query_params.get("path", "")
        files = self.service(request.user, path)
        data = files.list()
        if data is None:
            return Response({"detail":"找不到指定路径"}, status=404)
        return Response(data)
    @list_route()
    def download(self, request):
        '''download'''
        path = request.query_params.get("path", "")
        files = self.service(request.user, path)
        data = files.download()
        if data is None:
            return Response({"detail":"找不到指定路径"}, status=404)
        response = StreamingHttpResponse(data.get("stream"))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(data.get("name"))
        return response

    # 上传文件,format=None
    def create(self, request):
        '''create'''
        file_obj = request.data['file']
        path = request.query_params.get("path", "")
        files = self.service(request.user, path)
        status = files.file_upload(str(file_obj), file_obj)
        return Response(status=status)

    @list_route(methods=['POST'])
    def rename(self, request):
        '''rename'''
        path = request.data.get("path", "")
        name = request.data.get("name", "")
        if path and name:
            files = self.service(request.user, path)
            return Response(files.rename(name))
        return Response({"detail":"请提供path和name"}, status=400)

    @list_route(methods=['POST'])
    def remove(self, request):
        '''remove'''
        path = request.data.get("path", "")
        # name = request.data.get("name","")
        if path:
            files = self.service(request.user, path)
            return Response(files.remove())
        return Response({"detail":"请提供path"}, status=400)

    @list_route(methods=['POST'])
    def mkdir(self, request):
        '''mkdir'''
        path = request.data.get("path", "")
        name = request.data.get("name", "")
        if name:
            files = self.service(request.user, path)
            return Response(status=files.mkdir(name))
        return Response({"detail":"请提供path和name"}, status=400)

    @list_route(methods=['POST'])
    def unzip(self, request):
        '''unzip'''
        path = request.data.get("path", "")
        if path:
            files = self.service(request.user, path)
            return Response(status=files.unzip())
        return Response({"detail":"请提供path"}, status=400)
