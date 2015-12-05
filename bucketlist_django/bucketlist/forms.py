from django import forms


class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)


class CreateBucketlistForm(forms.Form):
    name = forms.CharField(max_length=100)


class UpdateBucketlistForm(forms.Form):
    name = forms.CharField(max_length=100)
    id = forms.CharField(widget=forms.HiddenInput())


class DeleteBucketlistForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput())


class UpdateBucketlistItemForm(forms.Form):
    name = forms.CharField(max_length=100)
    done = forms.BooleanField()
    id = forms.CharField(widget=forms.HiddenInput())
