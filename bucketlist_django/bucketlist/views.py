from django.shortcuts import render
from bucketlist.models import Bucketlist, BucketlistItem
from bucketlist.serializers import BucketlistSerializer, BucketlistItemSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class BucketListView(APIView):
    '''manages read and creation of bucketlists'''
    def get(self, request, format=None):
        # fetch all bucketlists and serialize them
        bucketlists = Bucketlist.objects.all()
        serializer = BucketlistSerializer(bucketlists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = BucketlistSerializer(data=request.data)
        # create bucketlist if data is valid
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        serializer = BucketlistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BucketListDetailView(APIView):
    '''manages get, update and delete for individual bucketlists'''

    def get_object(self, id):
        '''returns an instance of a bucketlist object'''
        try:
            return Bucketlist.objects.get(id=id)
            import pdb; pdb.set_trace()
        except Bucketlist.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        '''returns an individual bucketlist'''
        bucketlist = self.get_object(id)
        serializer = BucketlistSerializer(bucketlist)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id, format=None):
        '''updates a bucketlist'''
        # get the bucketlist
        bucketlist = self.get_object(id)
        serializer = BucketlistSerializer(bucketlist,
                                          data={'name': request.data['name']},
                                          partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        # get the bucketlist and delete it
        bucketlist = self.get_object(id)
        if bucketlist is not None:
            bucketlist.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
