from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from bucketlist.forms import UserRegistrationForm, UserLoginForm,\
                             CreateBucketlistForm, UpdateBucketlistForm,\
                             DeleteBucketlistForm, UpdateBucketlistItemForm
from rest_framework.test import APIClient
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from bucketlist.models import Bucketlist, BucketlistItem


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
            return HttpResponseRedirect(reverse('frontend:homepage'))
        else:
            # send back form errors as messages
            for error in form.errors:
                messages.add_message(request, messages.ERROR, form.errors[error])

            return HttpResponseRedirect(reverse('frontend:homepage') + '#register')


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
        return HttpResponseRedirect(reverse('frontend:homepage'))

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
                    return HttpResponseRedirect(reverse('frontend:dashboard'))
                else:
                    # Return a 'disabled account' error message
                    error = 'This account has been disabled!'
                    messages.add_message(request, messages.ERROR, error)
                    return HttpResponseRedirect(reverse('frontend:homepage') + '#login')
            else:
                # Return an 'invalid login' error message.
                error = 'Invalid login credentials'
                messages.add_message(request, messages.ERROR, error)
                return HttpResponseRedirect(reverse('frontend:homepage') + '#login')
        else:
            # send back form errors as messages
            for error in form.errors:
                messages.add_message(request, messages.ERROR, form.errors[error])

            return HttpResponseRedirect(reverse('frontend:homepage') + '#login')


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

        return HttpResponseRedirect(reverse('frontend:dashboard'))


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

        return HttpResponseRedirect(reverse('frontend:dashboard'))


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

        return HttpResponseRedirect(reverse('frontend:dashboard'))


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

    def post(self, request, id):
        '''create a bucketlist item'''
        # get the bucketlist object
        bucketlist = get_object_or_404(Bucketlist, pk=id)

        # validate form
        form = CreateBucketlistForm(request.POST)

        if form.is_valid():
            item_name = form.cleaned_data['name']

            # create and save bucketlist item
            item = BucketlistItem(name=item_name, bucketlist=bucketlist)
            item.save()

            # create success message
            messages.add_message(request,
                                 messages.INFO,
                                 'Bucketlist item created')
        else:
            # send back form errors as messages
            for error in form.errors:
                messages.add_message(request,
                                     messages.ERROR,
                                     form.errors[error])
        return HttpResponseRedirect(reverse('frontend:bucketlist_items', kwargs={'id': id}))


class UpdateBucketlistItemView(View):
    ''' updates a bucketlist item'''

    def post(self, request, id):
        '''update a bucketlist item'''

        # validate submitted form
        form = UpdateBucketlistItemForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            item_id = form.cleaned_data['id']
            done = form.cleaned_data['done']

            # get bucketlist item
            item = BucketlistItem.objects.get(id=item_id)

            # update and save item
            item.name = name
            item.done = done
            item.save()

            # set success message
            messages.add_message(request,
                                 messages.INFO,
                                 'Bucketlist Item updated.')
        else:
            # send back form errors as messages
            for error in form.errors:
                messages.add_message(request,
                                     messages.ERROR,
                                     form.errors[error])

        return HttpResponseRedirect(reverse('frontend:bucketlist_items', kwargs={'id': id}))


class DeleteBucketlistItemView(View):
    '''deletes a bucketlist item'''

    def post(self, request, id):
        '''delete a bucketlist item'''
        # validate form
        form = DeleteBucketlistForm(request.POST)

        if form.is_valid():
            item_id = form.cleaned_data['id']

            # get bucketlist item and delete
            item = BucketlistItem.objects.get(id=item_id)
            item.delete()

            # set success message
            messages.add_message(request,
                                 messages.INFO,
                                 'Bucketlist Item deleted')
        else:
            # send back form errors as messages
            for error in form.errors:
                messages.add_message(request,
                                     messages.ERROR,
                                     form.errors[error])
        return HttpResponseRedirect(reverse('frontend:bucketlist_items', kwargs={'id': id}))
