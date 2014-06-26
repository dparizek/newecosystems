from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from apps.core.serializers import *
from apps.core.models import *
from django.db.models import Q
from django.db import transaction
import decimal
import json


class CurrentUser(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        user = User.objects.get(id=request.user.id)
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)


class UserLabAccounts(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        lab_group = request.user.profile.lab_group.all()
        serializer = LabGroupSerializer(lab_group, many=True)
        return Response(serializer.data)


class MyPlants(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        p = Plant.objects.all()
        plants = PlantSerializer(p, many=True)
        return Response(plants.data)


class AllPlants(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        p = Plant.objects.all()
        plants = PlantSerializer(p, many=True)
        return Response(plants.data)


class UpdateTags(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def patch(self, request, pk, format=None):
        submission = get_object_or_404(Submission, pk=pk)
        tags = submission.tags.all()
        new_tags = request.DATA['tags']
        to_add = list()
        to_delete = list()
        for tag in tags:
            found = False
            for ntag in new_tags:
                if tag.id == ntag['id']:
                    found = True
            if not found:
                to_delete.append(tag)
        for tag in new_tags:
            if tag['id'] == 'new':
                to_add.append(tag)

        with transaction.atomic():
            for item in to_delete:
                submission.tags.remove(item)

            for item in to_add:
                submission.tags.add(item['name'])

        return Response('Tags for Submission ID "{0}" saved successfully.'.format(pk))


##REST File Upload for Submission
class SubmissionFileUpload(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = UploadedFile.objects.none()
    serializer_class = UploadedFileSerializer

    pk_url_kwarg = 'pk'

    def get_queryset(self):
        """
        This view returns a list of all uploaded files for a submission <pk>
        @todo: need to check for access permission so we don't give out files
        """
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        if pk is not None:
            ## here we need to check if user has access or not!
            return UploadedFile.objects.filter(submissionfk__pk=pk)
        else:
            return UploadedFile.objects.none()

    def pre_save(self, obj, request):
        """
        We override our submissionfk, uploadedby & file_description here
        """
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        if pk is not None:
            obj.submissionfk = get_object_or_404(Submission, pk=pk)
            obj.uploaded_by_who = request.user
            obj.file_description = ""
        else:
            ## TODO: we need to give up and 404 or something
            pass

    def post(self, request, format=None, *args, **kwargs):
        """
        We need insert our own pre_save call...
        """
        serializer = self.get_serializer(data=request.DATA, files=request.FILES, partial=True)
        if serializer.is_valid():
            self.pre_save(serializer.object, request)
            self.object = serializer.save(force_insert=True)
            self.post_save(self.object, created=True)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
