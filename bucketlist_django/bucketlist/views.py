from django.shortcuts import render, get_object_or_404
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
from django.views.generic import View
from bucketlist.forms import UserRegistrationForm, UserLoginForm,\
                             CreateBucketlistForm, UpdateBucketlistForm,\
                             DeleteBucketlistForm
from rest_framework.test import APIClient
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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


class HomePageView(View):
    '''handles homepage requests'''
    template_name = 'bucketlist/index.html'

    def get(self, request):
        return render(request, self.template_name)


class RegisterView(View):
    '''handles user registration'''

    def post(self, request):
        '''creates a new user'''

        # create an instance of user registration form
        form = UserRegistrationForm(request.POST)

        # validate form
        if form.is_valid():
            # create the user
            user = User.objects.create_user(form.cleaned_data['username'],
                                            form.cleaned_data['email'],
                                            form.cleaned_data['password'])
            user.save()
            messages.add_message(request, messages.INFO, 'User: %s successfully created.' %(user.username))
            return HttpResponseRedirect(reverse('homepage'))
        else:
            # send back form errors as messages
            for error in form.errors:
                messages.add_message(request, messages.ERROR, form.errors[error])

            return HttpResponseRedirect(reverse('homepage') + '#register')


class LoginView(View):
    '''handles user login and logout'''

    def get(self, request):
        '''logout a user'''

        # logout an authenticated user
        if request.user.is_authenticated():
            logout(request)

            # Redirect to home page.
            info = 'You have been logged out'
            messages.add_message(request, messages.INFO, info)
        return HttpResponseRedirect(reverse('homepage'))

    def post(self, request):
        ''' authenticate and login a user '''

        form = UserLoginForm(request.POST)

        # validate form
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # authenticate user
            user = authenticate(username=username, password=password)
            if user is not None:
                # the password verified for the user
                if user.is_active:
                    login(request, user)

                    # Redirect to a success page.
                    return HttpResponseRedirect(reverse('dashboard'))
                else:
                    # Return a 'disabled account' error message
                    error = 'This account has been disabled!'
                    messages.add_message(request, messages.ERROR, error)
                    return HttpResponseRedirect(reverse('homepage') + '#login')
            else:
                # Return an 'invalid login' error message.
                error = 'Invalid login credentials'
                messages.add_message(request, messages.ERROR, error)
                return HttpResponseRedirect(reverse('homepage') + '#login')
        else:
            # send back form errors as messages
            for error in form.errors:
                messages.add_message(request, messages.ERROR, form.errors[error])

            return HttpResponseRedirect(reverse('homepage') + '#login')


class UserDashboardView(View):
    '''
    displays the user's dashboard, handles bucketlist display,
    creation, update and deletion
    '''
    template_name = 'bucketlist/dashboard.html'
    client = APIClient()

    def get(self, request):
        '''displays a user's dashboard'''
        # get all bucketlist that belong to the user
        bucketlist_objects = Bucketlist.objects.all().filter(created_by=request.user)

        # setup paginator
        paginator = Paginator(bucketlist_objects, 10)

        # get page being requested
        page = request.GET.get('page')
        try:
            bucketlists = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            bucketlists = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page
            bucketlists = paginator.page(paginator.num_pages)

        context = {'bucketlists': bucketlists,
                   'page_range': paginator.page_range}
        return render(request, self.template_name, context)

    def post(self, request):
        '''creates a bucketlist for a user'''

        # validate form
        form = CreateBucketlistForm(request.POST)

        if form.is_valid():
            bucketlist_name = form.cleaned_data['name']

            # create a new bucketlist
            new_bucketlist = Bucketlist(name=bucketlist_name,
                                        created_by=request.user)
            new_bucketlist.save()

            messages.add_message(request,
                                 messages.INFO,
                                 'Bucketlist successfully created.')
        else:
            # send back form errors as messages
            for error in form.errors:
                messages.add_message(request,
                                     messages.ERROR,
                                     form.errors[error])

        return HttpResponseRedirect(reverse('dashboard'))


class UpdateBucketlistView(View):

    def post(self, request):
        '''updates a bucketlist'''

        # validate form
        form = UpdateBucketlistForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            id = form.cleaned_data['id']

            # get bucketlist object and update it
            bucketlist = Bucketlist.objects.get(id=id)
            bucketlist.name = name
            bucketlist.save()

            # add success message
            messages.add_message(request,
                                 messages.INFO,
                                 'Bucketlist updated.')
        else:
            # send back form errors as messages
            for error in form.errors:
                messages.add_message(request,
                                     messages.ERROR,
                                     form.errors[error])

        return HttpResponseRedirect(reverse('dashboard'))


class DeleteBucketlistView(View):

    def post(self, request):
        '''delete a bucketlist'''

        # validate form
        form = DeleteBucketlistForm(request.POST)

        if form.is_valid():
            id = form.cleaned_data['id']

            # get bucketlist object and delete it
            bucketlist = Bucketlist.objects.get(id=id)
            bucketlist.delete()

            # add success message
            messages.add_message(request,
                                 messages.INFO,
                                 'Bucketlist deleted.')
        else:
            # send back form errors as messages
            for error in form.errors:
                messages.add_message(request,
                                     messages.ERROR,
                                     form.errors[error])

        return HttpResponseRedirect(reverse('dashboard'))


class BucketlistItemView(View):
    template_name = 'bucketlist/items.html'

    def get(self, request, id):
        '''display the items in a bucketlist'''
        # get the bucketlist object
        bucketlist = get_object_or_404(Bucketlist, pk=id)

        # get the list of items for this bucketlist
        items_object = bucketlist.bucketlistitems.all()

        # setup paginator
        paginator = Paginator(items_object, 10)

        # get page being requested
        page = request.GET.get('page')
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            items = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page
            items = paginator.page(paginator.num_pages)

        context = {'bucketlist': bucketlist, 'items': items}

        return render(request, self.template_name, context)
