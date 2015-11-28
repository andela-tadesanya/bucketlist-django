from rest_framework import serializers
from bucketlist.models import Bucketlist, BucketlistItem
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    bucketlists = serializers.PrimaryKeyRelatedField(many=True, queryset=Bucketlist.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'bucketlists')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class BucketlistItemSerializer(serializers.ModelSerializer):
    bucketlist = serializers.PrimaryKeyRelatedField(required=False, queryset=Bucketlist.objects.all())

    class Meta:
        model = BucketlistItem
        fields = ('id',
                  'name',
                  'date_created',
                  'date_modified',
                  'done',
                  'bucketlist')


class BucketlistSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(required=False)
    bucketlistitems = BucketlistItemSerializer(many=True, read_only=True)

    class Meta:
        model = Bucketlist
        fields = ('id',
                  'name',
                  'date_created',
                  'date_modified',
                  'bucketlistitems',
                  'created_by')
