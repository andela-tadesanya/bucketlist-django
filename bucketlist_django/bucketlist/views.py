from django.shortcuts import render
from bucketlist.models import Bucketlist, BucketlistItem
from bucketlist.serializers import BucketlistSerializer,\
            BucketlistItemSerializer, UserSerializer
from django.http import Http404
from django.core.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication,\
                    BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class UserDetail(generics.RetrieveAPIView):
    '''returns details of a user'''
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreate(generics.CreateAPIView):
    '''creates a user'''
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BucketListView(APIView):
    '''manages read and creation of bucketlists'''

    # sets authentication and permissions for this view
    authentication_classes = (SessionAuthentication,
                              BasicAuthentication,
                              TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        '''returns all the bucketlist of a user'''
        # fetch all bucketlists and serialize them
        bucketlists = Bucketlist.objects.all().filter(created_by=request.user)

        # check if bucketlists is empty
        if len(bucketlists) == 0:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            serializer = BucketlistSerializer(bucketlists, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        '''creates a bucketlist for the current user'''

        serializer = BucketlistSerializer(data=request.data)

        # create bucketlist if data is valid
        if serializer.is_valid():
            # attach the user to the bucketlist before saving
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BucketListDetailView(APIView):
    '''manages get, update and delete for individual bucketlists'''

    # sets authentication and permissions for this view
    authentication_classes = (SessionAuthentication,
                              BasicAuthentication,
                              TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self, id, user):
        '''returns an instance of a bucketlist object'''
        # get the bucketlist
        try:
            bucketlist = Bucketlist.objects.get(id=id)
        except Bucketlist.DoesNotExist:
            raise Http404

        # check if bucketlist belongs to this user
        if bucketlist.created_by != user:
            raise PermissionDenied
        else:
            return bucketlist

    def get(self, request, id, format=None):
        '''returns an individual bucketlist'''
        # get the bucketlist
        bucketlist = self.get_object(id, request.user)
        serializer = BucketlistSerializer(bucketlist)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id, format=None):
        '''updates a bucketlist'''
        # get the bucketlist
        bucketlist = self.get_object(id, request.user)
        serializer = BucketlistSerializer(bucketlist,
                                          data={'name': request.data['name']},
                                          partial=True)

        # validate serializer before saving
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        # get the bucketlist
        bucketlist = self.get_object(id, request.user)

        bucketlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BucketListItemListView(APIView):
    '''displays and creates items of a bucketlist'''

    # set authentication and permissions for this view
    authentication_classes = (SessionAuthentication,
                              BasicAuthentication,
                              TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self, id, user):
        '''returns an instance of a bucketlist object'''

        # get the bucketlist
        try:
            bucketlist = Bucketlist.objects.get(id=id)
        except Bucketlist.DoesNotExist:
            raise Http404

        # check if bucketlist belongs to this user
        if bucketlist.created_by != user:
            raise PermissionDenied
        else:
            return bucketlist

    def get(self, request, id, format=None):
        '''returns a list of items in a bucketlist'''

        # get the instance of the bucketlist
        bucketlist = self.get_object(id, request.user)

        # get items for the bucketlist
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

        # get the instance of the bucketlist
        bucketlist = self.get_object(id, request.user)

        # create serializer
        serializer = BucketlistItemSerializer(data=request.data)

        # create bucketlist if data is valid
        if serializer.is_valid():
            serializer.save(bucketlist=bucketlist)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BucketListItemDetailView(APIView):
    '''manages display, update and deletion of individual bucketlist items'''

    # set authentication and permissions for this view
    authentication_classes = (SessionAuthentication,
                              BasicAuthentication,
                              TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self, id, user):
        '''returns an instance of a bucketlist object'''

        # get the bucketlist
        try:
            bucketlist = Bucketlist.objects.get(id=id)
        except Bucketlist.DoesNotExist:
            raise Http404

        # check if bucketlist belongs to this user
        if bucketlist.created_by != user:
            raise PermissionDenied
        else:
            return bucketlist

    def get_item(self, item_id, bucketlist):
        '''returns an instance of a bucketlist item object'''
        # get the bucketlist item
        try:
            item = BucketlistItem.objects.filter(id=item_id).first()
        except BucketlistItem.DoesNotExist:
            raise Http404

        # check if item belongs to this bucketlist
        if item.bucketlist != bucketlist:
            raise PermissionDenied
        else:
            return item

    def get(self, request, id, item_id, format=None):
        '''returns a bucketlist item of a particular bucketlist'''

        # get the bucketlist object the item belongs to
        bucketlist = self.get_object(id, request.user)

        # get bucketlist items
        bucketlist_item = self.get_item(item_id, bucketlist)

        # create serializer
        serializer = BucketlistItemSerializer(bucketlist_item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id, item_id, format=None):
        '''updates a bucketlist item and returns it'''

        # get the bucketlist object the item belongs to
        bucketlist = self.get_object(id, request.user)

        # get the bucketlist item
        bucketlist_item = self.get_item(item_id, bucketlist)

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

        # get the bucketlist object the item belongs to
        bucketlist = self.get_object(id, request.user)

        # get the bucketlist item
        bucketlist_item = self.get_item(item_id, bucketlist)

        bucketlist_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
