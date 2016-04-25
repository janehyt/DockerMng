# -*- coding: UTF-8 -*- 
from django.contrib.auth.models import User
from rest_framework import serializers
from .docker_client import DockerClient
from  .models import Container


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'id','username', 'password','email')
    password = serializers.CharField(
    	style={'input_type': 'password'},
    	write_only = True
	)
    def create(self,validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self,instance,validated_data):
        instance.username=validated_data.get('username',instance.username)
        instance.email=validated_data.get('email',instance.email)
        if(validated_data['password']):
            instance.set_password(validated_data['password'])
        instance.save()
        return instance

class ContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = ('id','name','user','created','updated')
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)
    updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)