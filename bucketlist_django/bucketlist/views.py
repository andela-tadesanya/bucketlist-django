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

        # check if bucketlists is empty
        if len(bucketlists) == 0:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            serializer = BucketlistSerializer(bucketlists, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = BucketlistSerializer(data=request.data)
        # create bucketlist if data is valid
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BucketListDetailView(APIView):
    '''manages get, update and delete for individual bucketlists'''

    def get_object(self, id):
        '''returns an instance of a bucketlist object'''
        try:
            return Bucketlist.objects.get(id=id)
        except Bucketlist.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        '''returns an individual bucketlist'''
        bucketlist = self.get_object(id)

        # check if the bucketlist exists
        if bucketlist is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = BucketlistSerializer(bucketlist)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id, format=None):
        '''updates a bucketlist'''
        # get the bucketlist
        bucketlist = self.get_object(id)
        serializer = BucketlistSerializer(bucketlist,
                                          data={'name': request.data['name']},
                                          partial=True)

        # validate serializer before saving
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        # get the bucketlist and delete it
        bucketlist = self.get_object(id)
        bucketlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        


class BucketListItemListView(APIView):
    '''displays and creates items of a bucketlist'''

    def get_object(self, id):
        '''returns an instance of a bucketlist object'''
        try:
            return Bucketlist.objects.get(id=id)
        except Bucketlist.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        '''returns a list of items in a bucketlist'''
        # get the instance of the bucketlist
        bucketlist = self.get_object(id)

        # get bucketlist items
        bucketlist_items = BucketlistItem.objects.all().filter(bucketlist=bucketlist)

        # check if bucketlists is empty
        if len(bucketlist_items) == 0:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            # create serializer
            serializer = BucketlistItemSerializer(bucketlist_items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, id, format=None):
        '''creates a bucketlist item'''
        # create serializer
        serializer = BucketlistItemSerializer(data=request.data)
        # create bucketlist if data is valid
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BucketListItemDetailView(APIView):
    '''manages display, update and deletion of individual bucketlist items'''

    def get_item(self, id):
        '''returns an instance of a bucketlist item object'''
        try:
            return BucketlistItem.objects.get(id=id)
        except BucketlistItem.DoesNotExist:
            raise Http404

    def get(self, request, id, item_id, format=None):
        '''returns a bucketlist item of a particular bucketlist'''

        # get bucketlist items
        try:
            bucketlist_items = BucketlistItem.objects.get(id=item_id)
        except BucketlistItem.DoesNotExist:
            raise Http404

        # create serializer
        serializer = BucketlistItemSerializer(bucketlist_items)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id, item_id, format=None):
        '''updates a bucketlist item and returns it'''

        # get the bucketlist item
        bucketlist_item = self.get_item(item_id)

        # set done
        if 'done' in request.data and request.data['done'].lower() == 'true':
            done = True
        else:
            done = False

        # update serializer
        serializer = BucketlistItemSerializer(bucketlist_item,
                                              data={'name': request.data['name'], 'done': done},
                                              partial=True)
        # validate serializer before saving
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, item_id, format=None):
        '''deletes a bucketlist item'''
        # get the bucketlist item
        bucketlist_item = self.get_item(item_id)
        bucketlist_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
