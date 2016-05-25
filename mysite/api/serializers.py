'''serializers'''
# -*- coding: UTF-8 -*-
from django.contrib.auth.models import User
# from rest_framework.authtoken.models import Token
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Image, Repository, Process, Container,Port


class UserSerializer(serializers.ModelSerializer):
    '''UserSerializer'''
    class Meta:#pylint: disable=old-style-class,too-few-public-methods,no-init
        '''Meta'''
        model = User
        fields = ('url', 'id', 'username', 'password', 'email')
    password = serializers.CharField(\
    	style={'input_type': 'password'},\
    	write_only=True\
	)
    email = serializers.CharField(\
        validators=[UniqueValidator(queryset=User.objects.all())])
    # id = serializers.IntegerField(read_only=True)
    # url = serializers.CharField(read_only=True)
    def create(self, validated_data):
        '''create'''
        user = User(**validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user

    def update(self, instance, validated_data):
        '''update'''
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        if validated_data['password']:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance

class ImageSerializer(serializers.ModelSerializer):
    '''ImageSerializer'''
    class Meta:#pylint: disable=old-style-class,too-few-public-methods,no-init
        '''Meta'''
        model = Image
        fields = ('id', 'repository', 'status', 'detail', 'tag', 'isbuild', 'builddir')
    detail = serializers.CharField(read_only=True, source="get_status_display")
    builddir = serializers.CharField(write_only=True)

class RepoSerializer(serializers.ModelSerializer):
    '''RepoSerializer'''
    class Meta:#pylint: disable=old-style-class,too-few-public-methods,no-init
        '''Meta'''
        model = Repository
        fields = ('name', 'namespace', 'description', 'user', 'tag_count', 'created')
    # url = serializers.HyperlinkedField(lookup_field="name")
    created = serializers.DateTimeField(read_only=True)
    tag_count = serializers.IntegerField(source="tag_num", read_only=True)
    # description = serializers.CharField(write_only=True)

class ProcessSerializer(serializers.ModelSerializer):
    '''ProcessSerializer'''
    class Meta:#pylint: disable=old-style-class,too-few-public-methods,no-init
        '''Meta'''
        model = Process
        fields = ('pid', 'image', 'status', 'detail', 'proc')
    detail = serializers.DictField(source="get_detail", read_only=True)

# class EnvSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Environment
#         fields = ('id', 'key', 'value', 'container')

class ContainerSerializer(serializers.ModelSerializer):
    '''ContainerSerializer'''
    class Meta:
        model = Container
        fields = ('id', 'name', 'user', 'image', 'command', 'restart',\
            'created','updated', 'ports','binds','envs','links')
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)
    ports = serializers.CharField(source="display_ports")
    binds = serializers.CharField(source="display_binds")
    envs = serializers.CharField(source="display_environments")
    links = serializers.CharField(source="display_links")

    # environments = EnvSerializer

    def create(self, validated_data):
        '''create'''
        print validated_data
        return Container()

