from django.test import TestCase
from django.contrib.auth.models import User
from bucketlist.models import Bucketlist


# Create your tests here.
class BucketlistTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
                    username='jake',
                    email='jk@email.com',
                    password='fatman')
        Bucketlist.objects.create(name='checkpoint 1', created_by=self.user)

    def test_bucketlist_created_properly(self):
        '''Check bucketlist is created properly'''
        mylist = Bucketlist.object.get(name='checkpoint 1')
        self.assertIsNotNone(mylist)
        self.assertEqual(mylist.date_created, mylist.date_modified)
        self.assertIsNotNone(mylist.items)
        self.assertEqual(mylist.created_by, self.user)
