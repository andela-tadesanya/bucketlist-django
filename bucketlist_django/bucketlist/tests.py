from django.test import TestCase
from django.contrib.auth.models import User
from bucketlist.models import Bucketlist, BucketlistItem


# Create your tests here.
class BucketlistTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
                                             username='jake',
                                             email='jk@email.com',
                                             password='fatman')
        Bucketlist.objects.create(
                                  name='checkpoint 1',
                                  created_by=self.user)
        self.mylist = Bucketlist.objects.get(name='checkpoint 1')

        BucketlistItem.objects.create(
                                      name='write tests',
                                      done=False,
                                      bucketlist=self.mylist)
        self.listitem = BucketlistItem.objects.get(name='write tests')

    def test_bucketlist_created_properly(self):
        '''check bucketlist is created properly'''
        self.assertIsNotNone(self.mylist, msg='the bucketlist was not created')
        self.assertEqual(self.mylist.date_created,
                         self.mylist.date_modified,
                         msg='date_created is not equal to date_modified on creation of object')
        self.assertIsNotNone(
                             self.mylist.bucketlistitem_set.all(),
                             msg='no items were found for this bucketlist')
        self.assertEqual(self.mylist.created_by,
                         self.user,
                         msg='creator of the bucketlist is not correct')

    def test_bucketlist_item_created_properly(self):
        '''check bucketlist item is created properly'''
        self.assertIsNotNone(self.listitem,
                             msg='the bucketlist item does not exist')
        self.assertEqual(self.listitem.bucketlist,
                         self.mylist,
                         msg='incorrect bucketlist that owns this item')
        self.assertEqual(self.listitem.date_created,
                         self.listitem.date_modified,
                         msg='date_created is not equal to date_modified on creation of object')
        self.assertIsNotNone(self.listitem.id,
                             msg='bucketlist item has to id')

    def test_bucketlist_endpoint(self):
        '''test bucketlist endpoint is returning right data'''
        response = self.client.get('/api/v1.0/bucketlist/')
        self.assertIsNotNone(response)

    def test_bucketlist_item(self):
        '''test a bucketlist item endpoint returns correctly'''
        response = self.client.get('/api/v1.0/bucketlist/1/item/1')
        self.assertIsNotNone(response)
    