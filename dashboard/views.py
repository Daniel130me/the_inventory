from django.shortcuts import render, redirect
from user.models import get_user_model,Profile
from .forms import AddProductForm, OrderForm, CategoryForm
from django.http import JsonResponse
from .models import Product, Order,  Category
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from user.functions import sanitize_data

# Create your views here.
@login_required(login_url='user-login')
def index(request):
    if not request.user.is_staff:
        return redirect('customer')
    quantity = Order.objects.values_list('quantity', flat=True)
    total_quantity =  sum(list(int(int(int_quantity)) for int_quantity in quantity))
    products = Product.objects.values('name','quantity','image','category__category_name').order_by('-created_at')[:2]
    for product in products:
        product['image'] = product['image'].split("/")[-1] #get only image name without the folder name
    p_quantity = Product.objects.values_list('quantity', flat=True)
    total_product_quantity = sum(list(int(each_quantity) for each_quantity in p_quantity))

    orders = Order.objects.values('id','status','quantity','created_at','ordered_by_id__first_name','product_id_id__name','product_id_id__image','product_id_id__category__category_name').order_by('-created_at')[:2]
    users = get_user_model().objects.values('id','first_name', 'last_name', 'email', 'profile__phone','profile__image').filter(is_staff=True).order_by('first_name')
    
    context = {
        'products':products,
        'total_product':Product.objects.values('id').count(),
        'total_p_quantity':total_product_quantity,
        'users': users,
        'orders':orders,
        'total_orders':Order.objects.values('id').count(),
        'total_quantity':total_quantity,
    }
    return render(request, 'dashboard/index.html',context)

@login_required(login_url='user-login')
def products(request):
    categories = Category.objects.values('id','category_name').order_by('category_name')
    return render(request, 'dashboard/products.html',{'categories':categories})

def add_product(request):
    if request.method == 'POST':
        cleaned_data = sanitize_data(request.POST)
        form = AddProductForm(cleaned_data, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()

            return JsonResponse({'pg':['product_table'],'message':'success','info':'Added succesfully'})
        else:
            list_of_error = []
            for field, errors in form.errors.items():
                for error in errors:
                    list_of_error.append(error)
            return JsonResponse({'message':'.', 'info':list_of_error})

@ensure_csrf_cookie
def product_update(request):
    if request.method == 'POST':
        cleaned_data = sanitize_data(request.POST)
        form = AddProductForm(cleaned_data, request.FILES)
        if form.is_valid():
            pid = form.cleaned_data['id']
            product = Product.objects.get(id=pid)
            product.name = form.cleaned_data['name']
            product.category = form.cleaned_data['category']
            product.quantity = form.cleaned_data['quantity']
            product.image = form.cleaned_data['image']
            product.user_id = request.user
            product.save()
            return JsonResponse({'modal':'product_edit_modal','pg':['product_table'],'message':'success','info':'Updated succesfully'})
        else:
            list_of_error = []
            for field, errors in form.errors.items():
                for error in errors:
                    list_of_error.append(error)
            return JsonResponse({'message':'.', 'info':list_of_error})
            
#id=id of the user, value=actual data to be obtained through the id
def getuser(Id,value): 
    user = get_user_model().objects.get(id=Id)
    return getattr(user, value, None) #getattr() return value of an object. i takes in the object name, valuein the object to return and default value(value returned if the value needed is not in the object specified) 


def product_form(request):
    categories = Category.objects.values('id','category_name').order_by('category_name')
    return render(request, 'dashboard/product_form.html',{'categories':categories})

def product_table(request):
    products = Product.objects.values('id','name','category','quantity','image','created_at','user_id','user__id','user__first_name','category__category_name').order_by('-created_at')
    
    for product in products:
        product['image'] = product['image'].split("/")[-1] #get only image name without the folder name
    return render(request, 'dashboard/product_table.html', {'products':products})

def delete_product(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        product = Product.objects.get(id=id)
        product.delete()
        return JsonResponse({'modal':'delete_product_modal','pg':['product_table'],'message':'success','info':'Deleted succesfully'})


def category_details(request):
    categories = Category.objects.values('id','category_name')
    return render(request, 'dashboard/category_details.html', {'categories':categories})

def add_category(request):
    if request.method == 'POST':
        cleaned_data = sanitize_data(request.POST)
        form = CategoryForm(cleaned_data)
        if form.is_valid():
            category = form.save(commit=False)
            category.created_by = request.user
            category.save()
            return JsonResponse({'pg':['category_details','product_form'],'message':'success','info':'Added succesfully'})
        else:
            list_of_error = []
            for field, errors in form.errors.items():
                for error in errors:
                    list_of_error.append(error)
            return JsonResponse({'message':'.', 'info':list_of_error})

def delete_category(request):
    if request.method == 'POST':
        cleaned_data = sanitize_data(request.POST)
        category = Category.objects.get(id=cleaned_data['id'])
        category.delete()
        return JsonResponse({'modal':'category_action_modal','pg':['category_details','product_form'],'message':'success','info':'Deleted succesfully'})


def edit_category(request):
    if request.method == 'POST':
        cleaned_data = sanitize_data(request.POST)
        category = Category.objects.get(id=cleaned_data['id'])
        form  = CategoryForm(cleaned_data, instance=category)
        
        if form.is_valid():
            form.save()
            return JsonResponse({'modal':'category_action_modal','pg':['category_details','product_form'],'message':'success','info':'Added succesfully'})

        else:
            list_of_error = []
            for field, errors in form.errors.items():
                for error in errors:
                    list_of_error.append(error)
            return JsonResponse({'message':'.', 'info':list_of_error})


@login_required(login_url='user-login')
def order(request):
    return render(request, 'dashboard/order.html')



def order_table(request):
    orders = Order.objects.values('id','status','quantity','created_at','ordered_by_id__first_name','product_id_id__name','product_id_id__image','product_id_id__category__category_name',)
    return render(request, 'dashboard/order_table.html',{'orders':orders})

@ensure_csrf_cookie
def delete_order(request):
    cleaned_data = sanitize_data(request.POST)
    id = cleaned_data['id']
    order = Order.objects.get(id=id)
    order.delete()
    return JsonResponse({'modal':'delete_order_modal','pg':['order_table'],'message':'success','info':'Deleted succesfully'})

@ensure_csrf_cookie
def send_data(request):
    if request.method == 'POST':
        cleaned_data = sanitize_data(request.POST)
        id = cleaned_data['id']
        action = cleaned_data['action']
        value = cleaned_data['value']
        if action == 'staff_status':
            status = get_user_model().objects.get(id=id)
            status.is_active = value
            status.save()
        elif action == 'priviledge':
            status = get_user_model().objects.get(id=id)
            status.is_superuser = value
            status.save()
        elif action == 'order_status':
            status = Order.objects.get(id=id)
            status.status = value
            status.save()
        return JsonResponse({'message':'success'})
