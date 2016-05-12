# -*- coding: UTF-8 -*- 
from django.contrib.auth.models import User
from rest_framework import serializers
from .docker_client import DockerClient
from  .models import Container,Image,Progress


class UserSerializer(serializers.ModelSerializer):
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
        fields = ('id','name','user','status','image','command','ports','volumes',
            'links','envs','restart','created','updated')
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)
    # user = serializers.IntegerField()
    image = serializers.CharField()
    status = serializers.DictField(source='getDetailStatus', read_only=True)
    # repository = serializers.CharField(write_only=True)
    # def create(self,validated_data):
    #     repo = validated_data.get('image')
    #     user = validated_data.get('user')
    #     if repo:
    #         repos = repo.split(":")
    #         image_name = repos[0]
    #         image_tag = "latest"
    #         if len(repos)==2:
    #             image_tag = repo[1]
    #         print image_name+":"+image_tag

    #         image = Image.objects.get_or_create(name=image_name,tag=image_tag)
    #         print image[0].users
    #         # print image
    #         validated_data['image']=image[0]
    #     return Container(**validated_data)

class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = ('url','id','name','users','status','tag','created','updated')
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)
    # image = serializers.CharField(write_only=True)   
class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = ('pid','image','status','detail','pr')
    detail = serializers.DictField(source="getDetail",read_only=True)