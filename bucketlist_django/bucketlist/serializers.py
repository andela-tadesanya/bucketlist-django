from rest_framework import serializers
from bucketlist.models import Bucketlist


class BucketlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bucketlist
        fields = ('name',
                  'date_created',
                  'date_modified',
                  'created_by')
        
