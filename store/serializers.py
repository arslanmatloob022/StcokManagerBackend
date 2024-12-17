from ast import Store
from uuid import UUID
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from . models import CustomUser
from django.contrib.auth.models import  Group, Permission
from rest_framework import serializers




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        read_only_fields = (
            'groups',
            'user_permissions'
        )

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        if password and len(password) < 8:
            raise serializers.ValidationError({"status":False,"data": "Password must be at least 8 characters long."})
        

        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class logoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(max_length = 400)


class StoreSerializer(serializers.Serializer):
    class Meta:
        model = Store
        fields = '__all__'