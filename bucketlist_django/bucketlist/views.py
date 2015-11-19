from django.shortcuts import render
from bucketlist.models import Bucketlist, BucketlistItem
from bucketlist.serializers import BucketlistSerializer, BucketlistItemSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class BucketListView(APIView):
    '''list all bucketlists'''
    def get(self, request, format=None):
        bucketlists = Bucketlist.objects.all()
        serializer = BucketlistSerializer(bucketlists, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BucketlistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
