from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from bucketlist.models import Bucketlist, BucketlistItem
from rest_framework.test import APITestCase, APIClient, APIRequestFactory, force_authenticate
from django.core.urlresolvers import reverse
from rest_framework.authtoken.models import Token
from bucketlist.views import *



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
        self.assertIsNotNone(
                             self.mylist.bucketlistitems.all(),
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
        self.assertIsNotNone(self.listitem.id,
                             msg='bucketlist item has to id')


class BucketlistEndpointTestCase(APITestCase):

    @classmethod
    def setUpClass(self):
        self.user = User.objects.create_user(
                                             username='john',
                                             email='johndoe@email.com',
                                             password='kittylitter')
        Bucketlist.objects.create(
                                  name='checkpoint 2',
                                  created_by=self.user)

    @classmethod
    def tearDownClass(self):
        pass

    def test_01_bucketlist_endpoint(self):
        '''test get on bucketlist endpoint for non empty bucketlist'''
        token = Token.objects.get(user__username=self.user.username)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get(reverse('bucketlist:bucketlist_list'))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    def test_02_bucketlist_create(self):
        '''test if bucketlist can be created'''
        token = Token.objects.get(user__username=self.user.username)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = client.post(reverse('bucketlist:bucketlist_list'),
                               {'name': 'my list'},
                               format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('name', response.data,
                      msg='bucketlist name not in return data')
        self.assertIn('created_by', response.data,
                      msg='created_by user not in return data')
        self.assertIn('date_created', response.data,
                      msg='date_created not in return data')
        self.assertIn('date_modified', response.data,
                      msg='date_modified not in return data')
        self.assertEqual(response.data['name'], 'my list',
                         msg='incorrect name stored')

    def test_03_bucketlist_get_individual(self):
        '''test if an individual bucketlist can be fetched'''
        token = Token.objects.get(user__username=self.user.username)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        url = reverse('bucketlist:bucketlist_single', kwargs={'id': 1})
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_04_bucketlist_update(self):
        '''test bucketlist can be updated'''
        token = Token.objects.get(user__username=self.user.username)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        url = reverse('bucketlist:bucketlist_single', kwargs={'id': 1})
        data = {'name': 'our list'}
        response = client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('name', response.data,
                      msg='bucketlist name not in return data')
        self.assertIn('created_by', response.data,
                      msg='created_by user not in return data')
        self.assertIn('date_created', response.data,
                      msg='date_created not in return data')
        self.assertIn('date_modified', response.data,
                      msg='date_modified not in return data')
        self.assertEqual(response.data['name'], 'our list',
                         msg='incorrect name updated')

    def test_05_bucketlist_delete(self):
        '''test bucketlist can be deleted'''
        token = Token.objects.get(user__username=self.user.username)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        url = reverse('bucketlist:bucketlist_single', kwargs={'id': 1})
        response = client.delete(url)
        self.assertEqual(response.status_code, 204)


class UserEndpointTestCase(APITestCase):

    @classmethod
    def setUpClass(self):
        self.user = User.objects.create_user(
                                             username='trey',
                                             email='trey@email.com',
                                             password='kittylitter')

    @classmethod
    def tearDownClass(self):
        pass

    def test_01_create_user(self):
        '''test if a user can be created'''

        response = self.client.post(reverse('bucketlist:api_create_user'),
                                    {'username': 'auser',
                                     'password': 'mysecret',
                                     'email': 'auser@email.com'},
                                    format='json')
        self.assertEqual(response.status_code, 201)

    def test_02_get_user(self):
        '''test if a user's detail can be retrieved'''

        url = reverse('bucketlist:api_get_user', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class BucketlistItemEndpointTestCase(APITestCase):
    @classmethod
    def setUpClass(self):
        self.user = User.objects.create_user(
                                             username='jake3',
                                             email='jk3@email.com',
                                             password='fatman')
        Bucketlist.objects.create(name='checkpoint 3',
                                  created_by=self.user)
        self.mylist = Bucketlist.objects.get(name='checkpoint 3')

        BucketlistItem.objects.create(
                                      name='write tests 3',
                                      done=False,
                                      bucketlist=self.mylist)
        self.listitem = BucketlistItem.objects.get(name='write tests 3')

    @classmethod
    def tearDownClass(self):
        pass

    def test_01_bucketlistItem_get_all(self):
        '''tests if bucketlist items can be fetched'''
        token = Token.objects.get(user__username=self.user.username)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get(reverse('bucketlist:bucketlist_item_list',
                              kwargs={'id': self.mylist.id}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    def test_02_create_bucketlistItem(self):
        '''tests if bucketlist items can be created'''
        token = Token.objects.get(user__username=self.user.username)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        url = reverse('bucketlist:bucketlist_item_list',
                      kwargs={'id': self.mylist.id})
        data = {'name': 'write tests 3 a second time'}
        response = client.post(url, data, format='json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)

    def test_03_get_single_bucketlistItem(self):
        '''tests if a single bucketlist item can be fetched'''
        token = Token.objects.get(user__username=self.user.username)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        url = reverse('bucketlist:bucketlist_item_detail',
                      kwargs={'id': self.mylist.id,
                              'item_id': self.listitem.id})
        response = client.get(url)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    def test_04_update_bucketlistItem(self):
        '''tests if a bucketlist item can be update'''
        token = Token.objects.get(user__username=self.user.username)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        url = reverse('bucketlist:bucketlist_item_detail',
                      kwargs={'id': self.mylist.id,
                              'item_id': self.listitem.id})
        data = {'name': 'write tests 3 again',
                'done': 'true'}
        response = client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_05_delete_bucketlistItem(self):
        '''tests deletion of bucketlist item'''

        token = Token.objects.get(user__username=self.user.username)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        url = reverse('bucketlist:bucketlist_item_detail',
                      kwargs={'id': self.mylist.id,
                              'item_id': self.listitem.id})
        response = client.delete(url)
        self.assertEqual(response.status_code, 204)


class UserFrontendTestCase(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def tearDown(self):
        # logout user
        self.client.get(reverse('frontend:authentication'))

    def test_01_user_can_view_homepage(self):
        '''tests user can access homepage'''
        # Issue a GET request.
        response = self.client.get(reverse('frontend:homepage'))

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_02_user_can_register(self):
        '''tests user can register'''
        url = reverse('frontend:register_user')
        data = {'username': 'user6',
                'password': 'secret',
                'email': 'user6@yahoo.com'}
        response = self.client.post(url, data,  follow=True)
        self.assertEqual(response.status_code, 200)

    def test_03_user_can_login(self):
        '''tests user can login'''
        url = reverse('frontend:authentication')
        data = {'username': 'user6',
                'password': 'secret'}
        response = self.client.post(url, data,  follow=True)
        self.assertEqual(response.status_code, 200)

    def test_04_user_can_view_dashboard(self):
        '''tests user can access dashboard'''
        # create a user
        url = reverse('frontend:register_user')
        data = {'username': 'user7',
                'password': 'secret',
                'email': 'user6@yahoo.com'}
        response = self.client.post(url, data,  follow=True)

        # login a user
        url = reverse('frontend:authentication')
        data = {'username': 'user7',
                'password': 'secret'}
        response = self.client.post(url, data,  follow=True)

        # Issue a GET request to dashboard
        response = self.client.get(reverse('frontend:dashboard'))

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_05_user_can_create_bucketlist(self):
        '''tests a user can create a bucketlist'''
        # create a user
        url = reverse('frontend:register_user')
        data = {'username': 'user7',
                'password': 'secret',
                'email': 'user6@yahoo.com'}
        response = self.client.post(url, data,  follow=True)

        # login a user
        url = reverse('frontend:authentication')
        data = {'username': 'user7',
                'password': 'secret'}
        response = self.client.post(url, data,  follow=True)

        url = reverse('frontend:dashboard')
        data = {'name': 'my bucketlist 1'}
        response = self.client.post(url, data,  follow=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_06_user_can_update_bucketlist(self):
        '''tests user can update a bucketlist'''
        # create a user
        url = reverse('frontend:register_user')
        data = {'username': 'user7',
                'password': 'secret',
                'email': 'user6@yahoo.com'}
        response = self.client.post(url, data,  follow=True)

        # login a user
        url = reverse('frontend:authentication')
        data = {'username': 'user7',
                'password': 'secret'}
        response = self.client.post(url, data,  follow=True)

        # update a bucketlist
        url = reverse('frontend:update_bucketlist')
        data = {'name': 'my bucketlist 1 updated',
                'id': 1}
        response = self.client.post(url, data,  follow=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_07_user_can_add_bucketlist_item(self):
        '''tests user can create a bucketlist item'''
        # create a user
        url = reverse('frontend:register_user')
        data = {'username': 'user8',
                'password': 'secret',
                'email': 'user8@yahoo.com'}
        response = self.client.post(url, data,  follow=True)

        # login a user
        url = reverse('frontend:authentication')
        data = {'username': 'user8',
                'password': 'secret'}
        response = self.client.post(url, data,  follow=True)

        # create a bucketlist
        user = User.objects.get(username='user8')
        bucketlist = Bucketlist.objects.create(name='bucketlist for user 8',
                                               created_by=user)

        # create bucketlist item
        url = reverse('frontend:bucketlist_items', kwargs={'id': bucketlist.id})
        data = {'name': 'item 1'}
        response = self.client.post(url, data,  follow=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_08_user_can_view_bucketlist_item(self):
        ''' tests user can view his bucketlist items'''
        # create a user
        url = reverse('frontend:register_user')
        data = {'username': 'user9',
                'password': 'secret',
                'email': 'user9@yahoo.com'}
        response = self.client.post(url, data,  follow=True)

        # login a user
        url = reverse('frontend:authentication')
        data = {'username': 'user9',
                'password': 'secret'}
        response = self.client.post(url, data,  follow=True)

        # create a bucketlist
        user = User.objects.get(username='user9')
        Bucketlist.objects.create(name='bucketlist for user 9',
                                  created_by=user)

        # display bucketlist items
        url = reverse('frontend:bucketlist_items', kwargs={'id': 1})
        response = self.client.get(url)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_09_user_can_update_bucketlist_item(self):
        '''tests user can update a bucketlist item'''
        # create a user
        url = reverse('frontend:register_user')
        data = {'username': 'user10',
                'password': 'secret',
                'email': 'user10@yahoo.com'}
        response = self.client.post(url, data,  follow=True)

        # login a user
        url = reverse('frontend:authentication')
        data = {'username': 'user10',
                'password': 'secret'}
        response = self.client.post(url, data,  follow=True)

        # create a bucketlist
        user = User.objects.get(username='user10')
        bucketlist = Bucketlist.objects.create(name='bucketlist for user 10',
                                               created_by=user)

        # create bucketlist item
        url = reverse('frontend:bucketlist_items', kwargs={'id': bucketlist.id})
        data = {'name': 'item 1'}
        response = self.client.post(url, data,  follow=True)

        # update bucketlist item
        url = reverse('frontend:update_bucketlist_items', kwargs={'id': bucketlist.id})
        data = {'name': 'updated name',
                'id': 1,
                'done': 'true'}
        response = self.client.post(url, data,  follow=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_10_user_can_update_bucketlist_item(self):
        '''tests if user can delete a bucketlist item'''

        # create a user
        url = reverse('frontend:register_user')
        data = {'username': 'user11',
                'password': 'secret',
                'email': 'user11@yahoo.com'}
        response = self.client.post(url, data,  follow=True)

        # login a user
        url = reverse('frontend:authentication')
        data = {'username': 'user11',
                'password': 'secret'}
        response = self.client.post(url, data,  follow=True)

        # create a bucketlist
        user = User.objects.get(username='user11')
        bucketlist = Bucketlist.objects.create(name='bucketlist for user 11',
                                               created_by=user)

        # create bucketlist item
        url = reverse('frontend:bucketlist_items', kwargs={'id': bucketlist.id})
        data = {'name': 'item 1'}
        response = self.client.post(url, data,  follow=True)

        # delete bucketlist item
        url = reverse('frontend:delete_bucketlist_items',
                      kwargs={'id': bucketlist.id})
        data = {'id': 1}
        response = self.client.post(url, data,  follow=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_11_user_can_delete_bucketlist(self):
        '''tests user can delete a bucketlist'''
        # create a user
        url = reverse('frontend:register_user')
        data = {'username': 'user7',
                'password': 'secret',
                'email': 'user6@yahoo.com'}
        response = self.client.post(url, data,  follow=True)

        # login a user
        url = reverse('frontend:authentication')
        data = {'username': 'user7',
                'password': 'secret'}
        response = self.client.post(url, data,  follow=True)

        # delete a bucketlist
        url = reverse('frontend:delete_bucketlist')
        data = {'id': 1}
        response = self.client.post(url, data,  follow=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
