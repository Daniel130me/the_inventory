from django.shortcuts import render, redirect
from django.http import JsonResponse
from user.forms import RegistrationForm, User_update_form, ProfileForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model, authenticate, login,logout
from .models import Profile
from django.views.decorators.csrf import ensure_csrf_cookie
from .functions import sanitize_data
import os

  
def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard-index')
    else:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid(): # if email or username already does not exist or unique
                form.save()
                return JsonResponse({'url_to':'../login/','message': 'success'})
            else:
                return JsonResponse({'url_to':'../','message': 'User already exist!'})

        return render(request, 'user/register.html')

def signin(request):
    form = AuthenticationForm()
    if request.user.is_authenticated:
        return redirect('dashboard-index')
    else:
        if request.method == 'POST':
            email = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                
                request.session['company'] =  'Danny Store'
                print(os.environ.get("MYVAR"))
                # return redirect('dashboard-index')
                return JsonResponse({'url_to': '../', 'message':'success'})
            else:
                return JsonResponse({'message':'You do not have an account yet, Please register'})

    return render(request, 'user/login.html', {'form':form})


def signout(request):
    logout(request)
    return redirect('user-login')



def profile(request):
    if not request.user.is_staff:
        return render(request, 'customer/customer_profile.html')
    return render(request, 'user/profile.html')


def profile_update(request):
    if request.method == 'POST': 
        userform = User_update_form(request.POST, instance=request.user)
        profileform = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if userform.is_valid() and profileform.is_valid():
            userform.save()
            profileform.save()
            return JsonResponse({'modal':'profile_edit_modal','pg':['profile_details'],'message':'success','info':'Updated succesfully'})
        else:
            list_of_error = []
            for field, errors in userform.errors.items():
                for error in errors:
                    list_of_error.append(error)
            return JsonResponse({'message':'.', 'info':list_of_error})


def user(request):
    return render(request, 'user/user.html')
    

def user_page(request, pk):
    user_details = get_user_model().objects.get(id=pk)

    return render(request, 'user/user_page.html',{'user_details':user_details})

def user_table(request):
    users = get_user_model().objects.all().filter(is_staff=True).order_by('-date_joined')
    return render(request, 'user/user_table.html',{'users':users})


@ensure_csrf_cookie
def user_update(request):
    if request.method == 'POST':
        cleaned_data = sanitize_data(request.POST)
        id = cleaned_data['id']
        user = get_user_model().objects.get(id=id)
        profile = Profile.objects.get(staff_id=id)
        userform = User_update_form(cleaned_data, instance=user)
        profileform = ProfileForm(cleaned_data, request.FILES, instance=profile)
        if profileform.is_valid():
            profileform.save()
            userform.save()
            return JsonResponse({'modal':'user_edit_modal','pg':['user_table'],'message':'success','info':'Updated succesfully'})
        else:
            list_of_error = []
            for field, errors in userform.errors.items():
                for error in errors:
                    list_of_error.append(error)
            return JsonResponse({'message':'.', 'info':list_of_error})
    
@ensure_csrf_cookie
def delete_user(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        user = get_user_model().objects.get(id=id)
        user.delete()
        return JsonResponse({'modal':'delete_user_modal','pg':['user_table'],'message':'success','info':'Deleted succesfully'})


@ensure_csrf_cookie
def add_staff(request):
    if request.method == 'POST':
        cleaned_data = sanitize_data(request.POST)
        userform = User_update_form(request.POST)
        profileform = ProfileForm(cleaned_data, request.FILES)
        
        if userform.is_valid() and profileform.is_valid():
            user = userform.save(commit=False)
            user.is_active = True
            user.is_staff = True
            user.set_password(userform.cleaned_data['password1'])
            user.save()

            email = userform.cleaned_data['email']
            user_instance = get_user_model().objects.get(email=email)
            profile = Profile.objects.get(staff_id=user_instance.id)
            profile.phone = profileform.cleaned_data['phone']
            profile.address = profileform.cleaned_data['address']
            if profileform.cleaned_data['image'] != '':
                profile.image = profileform.cleaned_data['image']
            profile.save()
            return JsonResponse({'modal':'staff_add_modal','pg':['user_table'],'message':'success','info':'Added successfully'})
        
        else:
            list_of_error = []
            for field, errors in userform.errors.items():
                for error in errors:
                    list_of_error.append(error)
            return JsonResponse({'message':'.', 'info':list_of_error})


def profile_details(request):
    return render(request, "user/profile_details.html")