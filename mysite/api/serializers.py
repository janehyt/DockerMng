'''serializers'''
# -*- coding: UTF-8 -*-
import os
import datetime
from django.contrib.auth.models import User
from django.db import transaction
# from rest_framework.authtoken.models import Token
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Image, Repository, Process, Container, Volume, Bind,Creation
from .files import VolumeService


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
        fields = ('id','name', 'namespace', 'description', 'user', 'tag_count', 'created')
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

class ContainerSerializer(serializers.ModelSerializer):
    '''ContainerSerializer'''
    class Meta:
        model = Container
        fields = ('id', 'name', 'user', 'image', 'command', 'restart',\
            'created','updated', 'ports','binds','envs','links')
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)
    ports = serializers.CharField(source="display_ports",allow_blank=True)
    binds = serializers.CharField(source="display_binds",allow_blank=True)
    envs = serializers.CharField(source="display_environments",allow_blank=True)
    links = serializers.CharField(source="display_links",allow_blank=True)
    # image = serializers.CharField(source = "display_image")

    # environments = EnvSerializer

    def create(self, validated_data):
        '''create'''
        # print validated_data
        # try:
        with transaction.atomic():
            container = Container(name=validated_data['name'],\
                user=validated_data.get('user'),\
                command=validated_data.get('command'),\
                restart=validated_data.get('restart'),\
                image=validated_data.get('image'))
            container.save()
            if validated_data['display_ports']:
                container.create_ports(validated_data['display_ports'])
            if validated_data['display_environments']:
                container.create_environments(validated_data['display_environments'])
            if validated_data['display_links']:
                container.create_links(validated_data['display_links'])
            if validated_data['display_binds']:
                binds = validated_data['display_binds'].split(",")
                for b in binds:
                    data = b.split(":")
                    if len(data) is 2:
                        if data[0].startswith("/"):
                            volumes = Volume.objects.filter(path=data[0])
                            if len(volumes) is 1:
                                if volumes[0].private is False or volumes[0].user.id is container.user.id:
                                    bind = Bind(volume=volumes[0], path=data[1])
                                    container.binds.add(bind, bulk=False)
                        else:
                            volumes = Volume.objects.filter(name=data[0], user=container.user)
                            if len(volumes) is 1:                   
                                bind = Bind(volume=volumes[0], path=data[1])
                                container.binds.add(bind, bulk=False)
                            elif len(volumes) is 0:
                                files = VolumeService(container.user)
                                path = os.path.join(files.get_path(), data[0])
                                volume = Volume(name=data[0], user=container.user, private=True,path=path)
                                volume.save()
                                bind = Bind(volume=volume, path=data[1])
                                container.binds.add(bind, bulk=False)
            today = datetime.datetime.today()
            creation = Creation.objects.get_or_create(user = container.user,date=today)[0]
            creation.count +=1
            creation.save()
        return container

