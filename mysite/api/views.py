
# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import viewsets,renderers
from rest_framework.response import Response
# from rest_framework.renderers import BrowsableAPIRenderer,JSONRenderer,AdminRenderer
from rest_framework.decorators import permission_classes,detail_route,list_route
from api.serializers import UserSerializer, GroupSerializer
from rest_framework.permissions import AllowAny



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    # 重写创建用户
    # def perform_create(self,serializers):

    @list_route(methods=['POST'])
    @permission_classes((AllowAny,))
    def sign_in(self, request):
        # permission_classes=(AllowAny,)
        print(request.data)
        return Response("ok")

    @detail_route()
    def email(self, request):
        snippet = self.get_object()
        return Response(snippet.email)

    @list_route()
    def hello(self, request):
        return Response({"message": "Hello, world!"})


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer