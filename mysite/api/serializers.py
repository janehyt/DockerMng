# -*- coding: UTF-8 -*- 
from django.contrib.auth.models import User
# from rest_framework.authtoken.models import Token
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'id','username', 'password','email')
    password = serializers.CharField(
    	style={'input_type': 'password'},
    	write_only = True
	)
    email = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())])
    id = serializers.IntegerField(read_only=True)
    url = serializers.IntegerField(read_only=True)
    def create(self,validated_data):
        user = User(**validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user

    def update(self,instance,validated_data):
        instance.username=validated_data.get('username',instance.username)
        instance.email=validated_data.get('email',instance.email)
        if(validated_data['password']):
            instance.set_password(validated_data['password'])
        instance.save()
        return instance