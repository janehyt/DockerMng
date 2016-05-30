# -*- coding: UTF-8 -*-
'''views'''
# import json
# from collections import OrderedDict
import markdown
import calendar
import datetime
from collections import OrderedDict
from django.shortcuts import get_object_or_404
# Create your views here.
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import StreamingHttpResponse
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import AllowAny
from rest_framework.reverse import reverse
from docker import errors
from .serializers import UserSerializer, ImageSerializer,\
RepoSerializer, ProcessSerializer, ContainerSerializer
from .files import VolumeService
from .dockerconn import DockerHub, DockerClient
from .models import Image, Repository, Process, Container,Volume
from .helper import ImageHelper, ContainerHelper

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

    @list_route()
    def overview(self,request):
        user = request.user
        files = VolumeService(user)
        result={
            "images":user.images.all().count(),\
            "containers":{"total":user.containers.count(),\
            "pie":{"running":0, "error":0, "exited":0, "none":user.containers.count()}},\
            "files_size":files.get_size(),\
            "user":str(user)\
        }

        date = user.dates.all().order_by('date')
        
        result["containers"]["date"] = self.__resloveDate(date)

        cli = DockerClient().get_client()
        containers = user.containers.all()
        try:
            docker=cli.version()
        except errors.APIError:
            pass
        else:
            result["docker"] = {"version":docker["Version"], "api":docker["ApiVersion"]}

        for c in containers:
            try:
                sta = cli.inspect_container(c.name)["State"]["Status"]
            except errors.NotFound:
                pass
            else:
                result["containers"]["pie"]["none"] -= 1
                if sta in result["containers"]["pie"]:
                    result["containers"]["pie"][sta] += 1

        return Response(result)

    def __resloveDate(self,date):
        container_date = []
        today = datetime.date.today()
        min_date = max_date = today
        # print today.year,today.month,today.day
        if len(date) > 0:
            min_date = date[0].date
        index = 0
        while min_date <= max_date:
            count = 0
            for i in range(index, len(date)):
                if min_date == date[i].date:
                    count = date[i].count
                    index += 1
                break
            container_date.append([calendar.timegm(min_date.timetuple())*1000, count])
            min_date += datetime.timedelta(1)
        return container_date

class ContainerViewSet(viewsets.ViewSet):

    queryset = Container.objects.all().order_by('-created')
    serializer_class = ContainerSerializer
    pagination_class = StandardResultsSetPagination
    helper_class = ContainerHelper

    def list(self, request):
        pagination = self.pagination_class()
        query = request.query_params.get("query", "")
        queryset = Container.objects.filter(user=request.user, name__contains=query)
        data = pagination.paginate_queryset(queryset, request)

        serializer = ContainerSerializer(data, many=True, context={'request': request})
        containers = serializer.data
        cli = DockerClient().get_client()
        for container in containers:
            container["image"] = unicode(Image.objects.get(id=container["image"]))
            try:
                c = cli.inspect_container(container["name"])["State"]["Status"]
                container["status"]= c
            except errors.NotFound:
                container["status"] = "none"

            container["actions"] = self.__actions(container["status"],\
                container["id"],request)
        return pagination.get_paginated_response(containers)

    def create(self,request):
        '''create'''
        data = request.data
        print data
        data['user'] = request.user.id
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        # try:
        result = serializer.save()
        helper = self.helper_class(result)
        helper.run()
        return Response(self.serializer_class(result).data)
        # except Exception,e:
        #     return Response({"detail":"创建失败,请检查数据"},status=400)
        

    def retrieve(self, request, pk=None):
        data = get_object_or_404(self.queryset, pk=pk,user=request.user)
        helper = self.helper_class(data)
        result = helper.detail()
        # result["image"] = unicode(Image.objects.get(id=result["image"]))
        if result["status"] == 200:
            inspect = result["data"]["inspect"]
            status = inspect["State"]["Status"] if inspect else "none"
            result["data"]["actions"] = self.__actions(status, pk, request)
        return Response(**result)


    def destroy(self, request, pk=None):
        container = get_object_or_404(self.queryset, pk=pk,user=request.user)
        helper = self.helper_class(container)

        return Response(**helper.destroy())

    @list_route()
    def options(self,request):
        data={"links":[],"binds":[]}
        links = Container.objects.filter(user=request.user)
        for link in links:
            data["links"].append(link.name)
        binds = Volume.objects.filter(Q(user=request.user)|Q(private=False))
        for bind in binds:
            if bind.private:
                data["binds"].append(bind.name)
            else:
                data["binds"].append(bind.path)
        return Response(data)


    @detail_route()
    def stat(self, request, pk=None):
        container = get_object_or_404(self.queryset, pk=pk,user=request.user)
        helper = self.helper_class(container)

        return Response(**helper.stat())

    @detail_route(methods=["POST"])
    def run(self, request, pk=None):
        container = get_object_or_404(self.queryset, pk=pk,user=request.user)
        helper = self.helper_class(container)

        return Response(**helper.run())

    @detail_route(methods=["POST"])
    def stop(self, request, pk=None):
        container = get_object_or_404(self.queryset, pk=pk,user=request.user)
        helper = self.helper_class(container)

        return Response(**helper.stop())

    @detail_route(methods=["POST"])
    def pause(self, request, pk=None):
        container = get_object_or_404(self.queryset, pk=pk,user=request.user)
        helper = self.helper_class(container)

        return Response(**helper.pause())

    @detail_route(methods=["POST"])
    def unpause(self, request, pk=None):
        container = get_object_or_404(self.queryset, pk=pk,user=request.user)
        helper = self.helper_class(container)

        return Response(**helper.unpause())

    @detail_route(methods=["POST"])
    def restart(self, request, pk=None):
        container = get_object_or_404(self.queryset, pk=pk,user=request.user)
        helper = self.helper_class(container)

        return Response(**helper.restart())


    def __actions(self, status, pk=None, request=None):
        actions = OrderedDict({"detail":{\
            "name":"detail",\
            "url": reverse("container-detail", args=[pk], request=request)}})
        action_delete = {"name":"delete",\
            "url": reverse("container-detail", args=[pk], request=request)}

        if status == "running":
            actions["stop"] = {"name":"stop",\
                "url":reverse("container-stop", args=[pk], request=request)}
            actions["restart"] = {"name":"restart",\
                "url": reverse("container-restart", args=[pk], request=request)}
            actions["pause"] = {"name":"pause",\
                "url": reverse("container-pause", args=[pk], request=request)}

        elif status == "paused":
            actions["unpause"] = {"name":"unpause",\
                "url": reverse("container-unpause", args=[pk], request=request)}
        elif status == "exited":
            actions["start"] = {"name":"start",\
                "url": reverse("container-run", args=[pk], request=request)}
            actions["delete"] = action_delete
        elif status == "none":
            actions["start"] = {"name":"create",\
                "url": reverse("container-run", args=[pk], request=request)}
            actions["delete"] = action_delete
        elif status == "restarting":
            actions["stop"] = {"name":"stop",\
                "url": reverse("container-stop", args=[pk], request=request)}
            actions["delete"] = action_delete
        else:#出错
            actions["delete"] = action_delete

        return actions

class ImageViewSet(viewsets.ViewSet):
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
        serializer = self.serializer_class(data, many=True,\
            context={'request': request})
        images = serializer.data
        return pagination.get_paginated_response(images)

    def retrieve(self, request, pk=None):
        data = get_object_or_404(self.queryset, pk=pk, users=request.user)
        return Response(self.serializer_class(data).data)

    def destroy(self, request, pk=None):
        '''destroy'''
        data = get_object_or_404(self.queryset, pk=pk, users=request.user)
        if Container.objects.filter(image=data).count() is 0:
            data.users.remove(request.user)
            if data.isbuild and data.repository.startswith(Repository.LOCAL+"/"):
                response = self.helper_class(data).destroy()
                return Response(response.get("data"), status= response.get("status"))        
            return Response(status=204)
        else:
            return Response({"detail":"请先删除使用该镜像创建的容器"},status = 400)

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
                response = self.helper_class(image).pull()
                if isinstance(response, Image):
                    return Response(self.serializer_class(response).data)
                return Response(response.get("data",""), status=response.get("status",404))
            return Response({"detail":"所选镜像来源为本地仓库，不需要拉取"},\
                status=400)
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
        #检查表单数据是否合适
        if repository and tag and builddir and\
        repository.startswith(Repository.LOCAL+"/"):
            res = Repository.objects.filter(namespace=Repository.LOCAL,\
                name=repository.split("/")[1])
            if len(res) is 1:
                data["builddir"] = builddir
                data["isbuild"] = True
                data["status"] = Image.BUILDING
                serializer = self.serializer_class(data=data)
                #创建Image对象，成功后开始构建
                if serializer.is_valid():
                    image = serializer.save()
                    image.users.add(user)
                    image.save()
                    response = self.helper_class(image).build()
                    if isinstance(response, Image):
                        return Response(self.serializer_class(response).data)
                    return Response(response.get("data", ""), status=response.get("status", 404))
                else:
                    return Response("该仓库下已存在该标签构建的镜像", status=400)
            else:
                pass
        return Response("请给出合适的repository、tag、path", status=400)
    @detail_route(methods=['POST'])
    def rebuild(self, request, pk=None):
        '''rebuild'''
        image = get_object_or_404(self.queryset, pk=pk, users=request.user)
        #检查表单数据是否合适
        if image.isbuild and image.repository.startswith(Repository.LOCAL+"/"):
            response = self.helper_class(image).build()
            if isinstance(response, Image):
                return Response(self.serializer_class(response).data)
            return Response(response.get("data", ""), status=response.get("status", 404))
            
        return Response("该镜像非本地构建", status=400)

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

    def destroy(self,request,pk=None):
        '''destroy'''
        data = get_object_or_404(self.queryset, pk=pk, user=request.user)
        serializer = self.serializer_class(data)
        if serializer.data["tag_count"] is 0:
            data.delete()
            return Response("删除成功",status=200)
        else:
            return Response({"detail":"请先删除仓库内构建的镜像"},status=400)

    @detail_route()
    def tags(self, request, pk=None):#pylint: disable=invalid-name
        '''tags'''
        namespace = request.query_params.get("namespace", "library")
        tag_name = request.query_params.get("name", "")

        if namespace == Repository.LOCAL:
            queryset = Image.objects.filter(repository=namespace+"/"+pk,\
                tag__contains=tag_name,users=request.user)
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
