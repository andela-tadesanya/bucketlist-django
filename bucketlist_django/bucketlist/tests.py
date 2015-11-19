from django.test import TestCase
from django.contrib.auth.models import User
from bucketlist.models import Bucketlist, BucketlistItem
from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse
import json


# Create your tests here.
class BucketlistTestCase(TestCase):

    @classmethod
    def setUpClass(self):
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

    @classmethod
    def tearDownClass(self):
        pass

    def test_01_bucketlist_created_properly(self):
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

    def test_02_bucketlist_item_created_properly(self):
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


class BucketlistEndpointTestCase(APITestCase):

    @classmethod
    def setUpClass(self):
        self.user = User.objects.create_user(
                                             username='john',
                                             email='johndoe@email.com',
                                             password='kittylitter')


    def test_create_bucketlist(self):
        '''ensure a bucketlist can be created'''
        url = reverse('bucketlist:bucketlists')
        data = json.dumps({'name': 'my list', 'created_by': 1})
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

# class BucketlistEndpointTestCase(TestCase):

#     @classmethod
#     def setUpClass(self):
#         self.user = User.objects.create_user(
#                                              username='john',
#                                              email='johndoe@email.com',
#                                              password='kittylitter')

#     @classmethod
#     def tearDownClass(self):
#         pass

#     def test_01_bucketlist_endpoint(self):
#         '''test bucketlist endpoint is returning right data'''
#         response = self.client.get('/api/v1.0/bucketlist/')
#         self.assertIsNotNone(response)
#         self.assertEqual(response.status_code, 200)

#     def test_02_bucketlist_create(self):
#         '''test if bucketlist can be created'''
#         response = self.client.post('/api/v1.0/bucketlist/', data={'name': 'my list', 'created_by': 2})
#         self.assertEqual(response.status_code, 201)
#         self.assertIn('name', response.data[0],
#                       msg='bucketlist name not in return data')
#         self.assertIn('created_by', response.data[0],
#                       msg='created_by user not in return data')
#         self.assertIn('date_created', response.data[0],
#                       msg='date_created not in return data')
#         self.assertIn('date_modified', response.data[0],
#                       msg='date_modified not in return data')
#         self.assertEqual(response.data[0]['name'], 'my list',
#                          msg='incorrect name stored')
#         self.assertEqual(response.data[0]['created_by'], 2,
#                          msg='incorrect user stored')
#         self.assertEqual(response.data[0]['date_created'],
#                          response.data[0]['date_modified'],
#                          msg='creation date does not match modified date')

#     def test_03_bucketlist_update(self):
#         '''test bucketlist can be updated'''
#         response = self.client.put('/api/v1.0/bucketlist/1',
#                                    {'name': 'our list'})
#         self.assertEqual(response.status_code, 202)
#         self.assertIn('name', response.data[0],
#                       msg='bucketlist name not in return data')
#         self.assertIn('created_by', response.data[0],
#                       msg='created_by user not in return data')
#         self.assertIn('date_created', response.data[0],
#                       msg='date_created not in return data')
#         self.assertIn('date_modified', response.data[0],
#                       msg='date_modified not in return data')
#         self.assertEqual(response.data[0]['name'], 'our list',
#                          msg='incorrect name updated')
#         self.assertEqual(response.data[0]['created_by'], 2,
#                          msg='incorrect user stored')
#         self.assertNotEqual(response.data[0]['date_created'],
#                             response.data[0]['date_modified'],
#                             msg='creation date does not match modified date')

#     def test_04_bucketlist_delete(self):
#         '''test bucketlist can be deleted'''
#         response = self.client.delete('/api/v1.0/bucketlist/1')
#         self.assertEqual(response.status_code, 204)

#     def test_bucketlist_item(self):
#         '''test a bucketlist item endpoint returns correctly'''
#         response = self.client.get('/api/v1.0/bucketlist/1/item/1')
#        self.assertIsNotNone(response)
