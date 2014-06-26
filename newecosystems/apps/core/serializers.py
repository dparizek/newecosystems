import logging
import pprint
import StringIO

from rest_framework import serializers
from rest_framework.exceptions import ParseError
from django.contrib.auth.models import User
from apps.core.models import *


class TagListSerializer(serializers.WritableField):

    def from_native(self, data):
        if type(data) is not list:
            raise ParseError("expected a list of data")
        return data

    def to_native(self, obj):
        if type(obj) is not list:
            return [obj.all().values()]
        return obj


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class UserDetailSerializer(serializers.ModelSerializer):
    user_permissions = serializers.SerializerMethodField('get_permissions')
    user_group = serializers.SerializerMethodField('get_groups')

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'user_permissions', 'user_group')

    def get_permissions(self, obj):
        return obj.get_all_permissions()

    def get_groups(self, obj):
        return obj.groups.all()


class PlantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plant
        fields = ('id', 'common_name', 'genus', 'species', 'habit', 'family', 'annualness_index', 'forb_to_tree_index', 'water_needs_index', 'commonality_index', 'flower_spring', 'flower_summer', 'flower_fall', 'flower_winter', 'firefly_url')


class UploadedFileSerializer(serializers.ModelSerializer):
    ## Add our model property 'filename'
    filename = serializers.CharField(source='filename', read_only=True)
    filesize = serializers.IntegerField(source='filesize', read_only=True)

    class Meta:
        model = UploadedFile
        depth = 2
