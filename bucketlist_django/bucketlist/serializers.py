from rest_framework import serializers
from bucketlist.models import Bucketlist, BucketlistItem


class BucketlistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bucketlist
        fields = ('id',
                  'name',
                  'date_created',
                  'date_modified',
                  'created_by')


class BucketlistItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = BucketlistItem
        fields = ('id',
                  'name',
                  'date_created',
                  'date_modified',
                  'done',
                  'bucketlist')
