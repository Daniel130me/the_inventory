from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import Profile

class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(required=False)
    password2 = forms.CharField(required=False)
    is_superuser = forms.CharField(required=False)

    """
    A Custom form for creating new users.
    """

    class Meta:
        model = get_user_model()
        fields = ["first_name","last_name","email", "password1", "password2",'is_superuser']

class Signin(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = ['email']

class ProfileForm(forms.ModelForm):
    phone = forms.CharField(required=False)
    address = forms.CharField(required=False)
    staff_id = forms.IntegerField(required=False)
    # image = forms.CharField(required=False)

    class Meta:
        model = Profile
        fields = ['phone', 'address', 'image', 'staff_id']#always write it as it is in database not in your model e.g. staff_id not staff

class User_update_form(forms.ModelForm):
    password1 = forms.CharField(required=False)
    # password2 = forms.CharField(required=False)
    # id = forms.CharField(required=False)
    # is_superuser = forms.CharField(required=False)
    class Meta:
        model = get_user_model()
        fields = ['email','first_name', 'last_name','password1']